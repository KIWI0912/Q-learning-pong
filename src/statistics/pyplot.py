import pandas as pd
import matplotlib.pyplot as plt

def analyze_game_stats():
    try:
        # Read CSV file
        print("Reading CSV file...")
        df = pd.read_csv('/Users/stella/Desktop/game_stats.csv')
        
        # Print DataFrame info for debugging
        print("\nDataFrame info:")
        print(df.info())
        print("\nFirst few rows:")
        print(df.head())
        
        # Check required columns
        required_columns = ['time', 'score']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Calculate statistics
        final_score = df['score'].iloc[-1]
        avg_score = df['score'].mean()
        max_score = df['score'].max()
        min_score = df['score'].min()
        game_duration = df['time'].iloc[-1]
        
        # Print analysis results
        print("\nGame Data Analysis:")
        print(f"Final Score: {final_score}")
        print(f"Average Score: {avg_score:.2f}")
        print(f"Highest Score: {max_score}")
        print(f"Lowest Score: {min_score}")
        print(f"Game Duration: {game_duration:.1f} seconds")
        
        # Create figures
        plt.figure(figsize=(12, 6))
        
        # Score over time plot
        plt.subplot(1, 2, 1)
        plt.plot(df['time'], df['score'], 'b-', label='Score Progress')
        plt.title('Score Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Score')
        plt.grid(True)
        plt.legend()
        
        # Score distribution histogram
        plt.subplot(1, 2, 2)
        plt.hist(df['score'], bins=20, color='skyblue', alpha=0.7)
        plt.title('Score Distribution')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.grid(True)
        
        # Adjust subplot layout
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('/Users/stella/Desktop/game_analysis.png')
        print("\nAnalysis plot saved to: /Users/stella/Desktop/game_analysis.png")
        
        # Display the plot
        plt.show()
        
    except FileNotFoundError:
        print("Error: game_stats.csv file not found")
        return
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty")
        return
    except Exception as e:
        print(f"Error during data analysis: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    analyze_game_stats()
