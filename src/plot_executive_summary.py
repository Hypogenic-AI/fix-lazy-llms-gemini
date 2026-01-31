import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Hardcoded data from previous analyses to ensure consistency for the summary plot
    strategies = ["Baseline", "Combined", "Skeptical"]
    avg_acc = [84.0, 89.0, 88.0]
    avg_len = [161.0, 291.1, 160.5]
    colors = ['gray', 'blue', 'green']
    
    plt.figure(figsize=(8, 6))
    
    # Scatter plot
    plt.scatter(avg_len, avg_acc, s=[300, 300, 300], c=colors, alpha=0.7)
    
    # Labels
    for i, name in enumerate(strategies):
        plt.text(avg_len[i], avg_acc[i]+0.5, name, ha='center', fontsize=12, fontweight='bold')
        
    # Arrows to show improvement
    plt.annotate("Brute Force (+5% Acc, +80% Cost)", 
                 xy=(avg_len[1], avg_acc[1]), xytext=(avg_len[0], avg_acc[1]),
                 arrowprops=dict(arrowstyle="->", color='blue', linestyle='dashed'), color='blue')
                 
    plt.annotate("Smart Prompt (+4% Acc, 0% Cost)", 
                 xy=(avg_len[2], avg_acc[2]), xytext=(avg_len[2], avg_acc[0]),
                 arrowprops=dict(arrowstyle="->", color='green'), color='green')

    plt.xlabel("Cost (Response Length in Words)")
    plt.ylabel("Performance (Average Accuracy %)")
    plt.title("Executive Summary: Strategy Efficiency")
    plt.grid(True, alpha=0.3)
    
    plt.savefig('results/executive_summary.png')
    print("Saved results/executive_summary.png")

if __name__ == "__main__":
    main()
