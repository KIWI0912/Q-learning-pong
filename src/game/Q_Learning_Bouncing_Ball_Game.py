import pygame
import random
import math

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Q-Learning Bouncing Ball Game")
clock = pygame.time.Clock()

f_big = pygame.font.Font(None, 48)
f_mid = pygame.font.Font(None, 32)
f_small = pygame.font.Font(None, 24)

# 以后有空加个保存加载Q表的功能，不然每次关了重开又变傻了
q_table = {}  

# 调了好几次的参数，目前这套比较顺手
# 挡板直接用全局变量，懒得写class了
pad_w = 100
pad_x = float(w // 2 - pad_w // 2)

class Ball:
    def __init__(self, x=None, y=None):
        self.x = float(x) if x is not None else float(random.randint(80, w - 80))
        self.y = float(y) if y is not None else 60.0
        self.vx = float(random.choice([-4, -3, 3, 4]))
        self.vy = float(random.choice([3, 4, 5]))
        self.r = 10
        
    def update(self):
        global pad_x, pad_w
        addscore = 0
        isLost = False
        self.x += self.vx
        self.y += self.vy
        
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx *= -1
        elif self.x + self.r >= w:
            self.x = w - self.r
            self.vx *= -1
            
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy *= -1
            
        # 挡板碰撞（之前老是卡在板子里疯狂鬼畜，加了 y - vy 判断好多了）
        top = h - 10
        if (self.vy > 0
                and pad_x <= self.x <= pad_x + pad_w
                and self.y + self.r >= top
                and self.y - self.vy <= top):
            self.y = top - self.r
            self.vy = -abs(self.vy)
            addscore += 5
            
            # 击球点偏离中心越多，横向速度改变越大
            offset = (self.x - (pad_x + pad_w / 2)) / (pad_w / 2)
            self.vx += offset * 1.2  # 0.8不够明显，改成1.2
            
            # 限速
            if self.vx > 6: self.vx = 6
            if self.vx < -6: self.vx = -6
            
        if self.y - self.r > h:
            isLost = True
            
        return addscore, isLost

class Star:
    def __init__(self):
        self.size = random.randint(20, 40)
        self.x = random.randint(100, w - 130)
        self.y = random.randint(90, h // 2)
        self.active = True
        self.stype = random.choice(["score", "extend", "extra_ball"])
        
    def checkHit(self, b):
        if not self.active: return None
        # 简单的矩形碰撞
        if self.x <= b.x <= self.x + self.size and self.y <= b.y <= self.y + self.size:
            self.active = False
            return self.stype
        return None

def drawStar(surf, cx, cy, radius, color):
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rr = radius if i % 2 == 0 else radius * 0.5
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    pygame.draw.polygon(surf, color, pts)

def getState(balls):
    global pad_x
    if not balls: return None
    
    # 找快掉出去的那个最危险的球
    down = [b for b in balls if b.vy > 0]
    if down:
        tgt = min(down, key=lambda b: (h - b.r - b.y) / (b.vy if b.vy != 0 else 1))
    else:
        tgt = balls[0]
        
    bx = int(tgt.x // 50)
    by = int(tgt.y // 50)
    px = int(pad_x // 50)
    dx = 1 if tgt.vx > 0 else -1
    dy = 1 if tgt.vy > 0 else -1
    
    side = sum(1 if b.x > tgt.x else -1 for b in balls if b is not tgt)
    return (bx, by, px, dx, dy, side)

def predictLand(balls):
    arr = []
    for b in balls:
        if b.vy <= 0: continue
        t = (h - b.r - b.y) / b.vy
        x = b.x + b.vx * t
        # 模拟墙壁反弹（一开始没加这个，球直接飞了）
        while x < 0 or x > w:
            if x < 0: x = -x
            elif x > w: x = 2 * w - x
        arr.append({"x": x, "t": t, "ref": b})
    arr.sort(key=lambda k: k["t"])
    return arr

def getAct(s, balls):
    global pad_x, pad_w
    if s not in q_table: q_table[s] = {-1: 0.0, 0: 0.0, 1: 0.0}
    
    preds = predictLand(balls)
    if not preds: return 0
        
    mid = pad_x + pad_w / 2
    wx = sum(it["x"] * (1.0 / (i + 1)) for i, it in enumerate(preds))
    tot_w = sum(1.0 / (i + 1) for i in range(len(preds)))
        
    tgt_x = wx / tot_w if tot_w > 0 else mid
    valid = [-1, 0, 1]
    
    if pad_x <= 0 and -1 in valid: valid.remove(-1)
    if pad_x + pad_w >= w and 1 in valid: valid.remove(1)
    
    # 80% 靠预测，20% 靠Q表，纯Q表前期太蠢了没法看一直在撞墙
    if random.random() < 0.8:
        dz = pad_w * 0.2
        if abs(tgt_x - mid) <= dz: return 0
        if tgt_x < mid: return -1 if -1 in valid else 0
        return 1 if 1 in valid else 0
        
    if random.random() < 0.1:
        return random.choice(valid)
        
    return max(valid, key=lambda a: q_table[s][a])

def calcReward(balls, act):
    global pad_x, pad_w
    preds = predictLand(balls)
    if not preds: return 0.0
        
    mid = pad_x + pad_w / 2
    r = 0.0
    # 调整几次之后留下的几个权重，目前看效果还行
    for i, it in enumerate(preds):
        wgt = 1.0 / (i + 1)
        dist = abs(it["x"] - mid)
        
        if it["x"] > mid and act == 1: r += 1.5 * wgt
        elif it["x"] < mid and act == -1: r += 1.5 * wgt
        elif dist < pad_w / 2 and act == 0: r += 2.0 * wgt
            
        if dist < pad_w:
            # 之前设的3.5，感觉不够，改成4.0
            r += ((pad_w - dist) / pad_w) * 4.0 * wgt
        elif dist > pad_w * 1.5:
            r -= 2.0 * wgt
    return r

def updateQ(s, a, r, ns):
    if s not in q_table: q_table[s] = {-1: 0.0, 0: 0.0, 1: 0.0}
    if ns not in q_table: q_table[ns] = {-1: 0.0, 0: 0.0, 1: 0.0}
    
    old = q_table[s][a]
    nxt = max(q_table[ns].values())
    q_table[s][a] = old + 0.1 * (r + 0.9 * nxt - old)


# ==========================================
# 主循环
# ==========================================
running = True
mode = "menu" 
balls = []
stars = [Star() for _ in range(10)]
score = 0
runTime = 0.0
star_t = 0
lastStar_t = 0

# 修复长按回车直接闪过菜单的问题
lock = False

while running:
    dt_ms = clock.tick(60)
    dt = dt_ms / 1000.0
    now = pygame.time.get_ticks()
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    if mode == "menu":
        screen.fill((255, 209, 220))
        t = f_mid.render("Q-Learning Bouncing Ball Game", True, (255, 20, 147))
        s = f_small.render("Press ENTER to Start", True, (255, 20, 147))
        e = f_small.render("Press ESC to Exit", True, (255, 20, 147))
        screen.blit(t, (w // 2 - t.get_width() // 2, 210))
        screen.blit(s, (w // 2 - s.get_width() // 2, 300))
        screen.blit(e, (w // 2 - e.get_width() // 2, 340))
        pygame.display.flip()
        
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_RETURN]:
            if not lock:
                lock = True
                mode = "game"
                pad_w = 100
                pad_x = float(w // 2 - pad_w // 2)
                balls = [Ball()]
                stars = [Star() for _ in range(10)]
                score = 0
                runTime = 0.0
                star_t = now
                lastStar_t = now
        else:
            lock = False
            
    elif mode == "game":
        if not balls:
            balls.append(Ball())
            
        s0 = getState(balls)
        if s0 is not None:
            a = getAct(s0, balls)
            # 之前设的4，太慢了
            pad_x += a * 5
            if pad_x < 0: pad_x = 0
            if pad_x + pad_w > w: pad_x = w - pad_w
        else:
            a = 0
            
        del_list = []
        for i, b in enumerate(balls):
            addscore, isLost = b.update()
            score += addscore
            
            for st in stars:
                tp = st.checkHit(b)
                if tp:
                    lastStar_t = now
                    if tp == "score":
                        score += 25
                    elif tp == "extend":
                        pad_w = min(200, pad_w + 30)
                    elif tp == "extra_ball":
                        if len(balls) < 3:  # 限制一下，不然满屏都是球卡死
                            balls.append(Ball(b.x, b.y))
                            
            if isLost:
                del_list.append(i)
                
        for idx in reversed(del_list):
            balls.pop(idx)
            
        if not balls:
            score -= 10
            balls.append(Ball())
            
        if now - lastStar_t >= 5000:
            score -= 10
            lastStar_t = now
            
        if now - star_t >= 10000:
            stars = [Star() for _ in range(10)]
            star_t = now
            
        s1 = getState(balls)
        if s0 is not None and s1 is not None:
            rr = calcReward(balls, a)
            updateQ(s0, a, rr, s1)
            
        runTime += dt
        timeLeft = 60.0 - runTime
        
        # 渲染画面
        screen.fill((255, 209, 220))
        for b in balls:
            pygame.draw.circle(screen, (255, 105, 180), (int(b.x), int(b.y)), b.r)
        pygame.draw.rect(screen, (255, 182, 193), (int(pad_x), h - 10, int(pad_w), 10))
        
        for s in stars:
            if s.active:
                cx = s.x + s.size // 2
                cy = s.y + s.size // 2
                drawStar(screen, cx, cy, s.size // 2, (255, 255, 0))
                
        t1 = f_small.render(f"Score: {score}", True, (255, 20, 147))
        t2 = f_small.render(f"Time: {max(0, int(timeLeft))}", True, (255, 20, 147))
        screen.blit(t1, (10, 10))
        screen.blit(t2, (w - 120, 10))
        
        pygame.display.flip()
        
        if timeLeft <= 0:
            mode = "over"
            
    elif mode == "over":
        screen.fill((255, 209, 220))
        t1 = f_big.render("Time's Up!", True, (255, 20, 147))
        t2 = f_mid.render(f"Your Score: {score}", True, (255, 20, 147))
        t3 = f_small.render("Press R to Return Menu", True, (255, 20, 147))
        t4 = f_small.render("Press ESC to Exit", True, (255, 20, 147))
        screen.blit(t1, (w // 2 - t1.get_width() // 2, 180))
        screen.blit(t2, (w // 2 - t2.get_width() // 2, 270))
        screen.blit(t3, (w // 2 - t3.get_width() // 2, 360))
        screen.blit(t4, (w // 2 - t4.get_width() // 2, 400))
        pygame.display.flip()
        
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_r]:
            if not lock:
                lock = True
                mode = "menu"
        else:
            lock = False
            
pygame.quit()
