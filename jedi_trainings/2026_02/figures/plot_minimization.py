"""
Parse and visualize cost function convergence from JEDI variational log files.

This script extracts J (total cost), Jb (background term), and Jo (observation term)
from a JEDI 3DVar/3DEnVar log file and creates diagnostic plots.
"""

import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def parse_variational_log(log_file):
    """
    Parse JEDI variational log file to extract cost function values.
    
    Parameters
    ----------
    log_file : str or Path
        Path to the JEDI log file
        
    Returns
    -------
    dict
        Dictionary containing arrays of iterations, J, Jb, Jo, and norm_reduction
    """
    iterations = []
    J_values = []
    Jb_values = []
    Jo_values = []
    norm_dict = {}
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        # Look for cost function values
        if 'Quadratic cost function: J   (' in line:
            # Extract iteration number and J value
            match = re.search(r'J\s+\(\s*(\d+)\)\s*=\s*([\d.e+-]+)', line)
            if match:
                iteration = int(match.group(1))
                J = float(match.group(2))
                
                # Get Jb from next line
                if i + 1 < len(lines):
                    jb_match = re.search(r'Jb\s+\(\s*\d+\)\s*=\s*([\d.e+-]+)', lines[i + 1])
                    if jb_match:
                        Jb = float(jb_match.group(1))
                    else:
                        Jb = np.nan
                
                # Get Jo from line after that
                if i + 2 < len(lines):
                    jo_match = re.search(r'JoJc\(\s*\d+\)\s*=\s*([\d.e+-]+)', lines[i + 2])
                    if jo_match:
                        Jo = float(jo_match.group(1))
                    else:
                        Jo = np.nan
                
                iterations.append(iteration)
                J_values.append(J)
                Jb_values.append(Jb)
                Jo_values.append(Jo)
        
        # Look for norm reduction values
        if 'Norm reduction (' in line:
            match = re.search(r'Norm reduction\s+\(\s*(\d+)\)\s*=\s*([\d.e+-]+)', line)
            if match:
                norm_iter = int(match.group(1))
                norm_val = float(match.group(2))
                norm_dict[norm_iter] = norm_val
    
    # Build norm_reductions aligned with iterations
    norm_reductions = np.array([norm_dict[i] for i in iterations if i in norm_dict])

    return {
        'iteration': np.array(iterations),
        'J': np.array(J_values),
        'Jb': np.array(Jb_values),
        'Jo': np.array(Jo_values),
        'norm_reduction': norm_reductions
    }


def plot_cost_function_convergence(data, output_file=None):
    """
    Create diagnostic plots for cost function convergence.
    
    Parameters
    ----------
    data : dict
        Dictionary with iteration, J, Jb, Jo, and norm_reduction arrays
    output_file : str or Path, optional
        If provided, save figure to this file
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('JEDI Variational Cost Function Convergence', fontsize=16, fontweight='bold')
    
    iteration = data['iteration']
    J = data['J']
    Jb = data['Jb']
    Jo = data['Jo']
    norm_reduction = data['norm_reduction']
    
    # Plot 1: Total cost function J
    ax1 = axes[0, 0]
    ax1.plot(iteration, J, 'o-', linewidth=2, markersize=4, color='black', label='J total')
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Cost Function J', fontsize=12)
    ax1.set_title('Total Cost Function Convergence', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    
    # Add percentage reduction text
    if len(J) > 1:
        J_reduction = (J[0] - J[-1]) / J[0] * 100
        ax1.text(0.95, 0.95, f'Reduction: {J_reduction:.1f}%',
                transform=ax1.transAxes, fontsize=11,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Jb and Jo separately
    ax2 = axes[0, 1]
    ax2.plot(iteration, Jb, 'o-', linewidth=2, markersize=4, 
             color='tab:blue', label='Jb (background term)')
    ax2.plot(iteration, Jo, 's-', linewidth=2, markersize=4, 
             color='tab:orange', label='Jo (observation term)')
    ax2.set_xlabel('Iteration', fontsize=12)
    ax2.set_ylabel('Cost Function Components', fontsize=12)
    ax2.set_title('Background vs Observation Terms', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    
    # Plot 3: Jb/Jo ratio (balance between terms)
    ax3 = axes[1, 0]
    # Avoid division by zero
    ratio = np.divide(Jb, Jo, where=Jo!=0, out=np.full_like(Jb, np.nan))
    ax3.plot(iteration, ratio, 'o-', linewidth=2, markersize=4, color='tab:green')
    ax3.set_xlabel('Iteration', fontsize=12)
    ax3.set_ylabel('Jb / Jo Ratio', fontsize=12)
    ax3.set_title('Balance Between Background and Observations', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0.1, color='gray', linestyle='--', alpha=0.5, label='Jb/Jo = 0.1')
    ax3.legend(fontsize=10)
    
    # Plot 4: Gradient norm reduction (log scale)
    ax4 = axes[1, 1]
    if len(norm_reduction) > 0:
        ax4.semilogy(iteration[:len(norm_reduction)], norm_reduction, 
                     'o-', linewidth=2, markersize=4, color='tab:red')
        ax4.axhline(y=1e-10, color='gray', linestyle='--', alpha=0.7, 
                   label='Convergence threshold (1e-10)')
        ax4.set_xlabel('Iteration', fontsize=12)
        ax4.set_ylabel('Gradient Norm Reduction', fontsize=12)
        ax4.set_title('Convergence Criterion', fontsize=13, fontweight='bold')
        ax4.grid(True, alpha=0.3, which='both')
        ax4.legend(fontsize=11)
        
        # Mark convergence iteration
        converged_idx = np.where(norm_reduction < 1e-10)[0]
        if len(converged_idx) > 0:
            conv_iter = iteration[converged_idx[0]]
            ax4.axvline(x=conv_iter, color='green', linestyle=':', alpha=0.7, linewidth=2)
            ax4.text(conv_iter, ax4.get_ylim()[1]*0.5, f'  Converged\n  (iter {conv_iter})',
                    fontsize=10, color='green', fontweight='bold')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.show()


def print_summary(data):
    """
    Print summary statistics of the minimization.
    
    Parameters
    ----------
    data : dict
        Dictionary with iteration, J, Jb, Jo, and norm_reduction arrays
    """
    print("\n" + "="*70)
    print("JEDI VARIATIONAL CONVERGENCE SUMMARY")
    print("="*70)
    
    iteration = data['iteration']
    J = data['J']
    Jb = data['Jb']
    Jo = data['Jo']
    norm_reduction = data['norm_reduction']
    
    print(f"\nInitial state (iteration 0):")
    print(f"  J  = {J[0]:.2f}")
    print(f"  Jb = {Jb[0]:.2f}")
    print(f"  Jo = {Jo[0]:.2f}")
    
    print(f"\nFinal state (iteration {iteration[-1]}):")
    print(f"  J  = {J[-1]:.2f}")
    print(f"  Jb = {Jb[-1]:.2f}")
    print(f"  Jo = {Jo[-1]:.2f}")
    
    print(f"\nCost function reduction:")
    J_reduction = J[0] - J[-1]
    J_percent = (J_reduction / J[0]) * 100
    print(f"  ΔJ  = {J_reduction:.2f} ({J_percent:.1f}%)")
    
    Jo_reduction = Jo[0] - Jo[-1]
    Jo_percent = (Jo_reduction / Jo[0]) * 100
    print(f"  ΔJo = {Jo_reduction:.2f} ({Jo_percent:.1f}%)")
    
    print(f"\nMinimization details:")
    print(f"  Total iterations: {len(iteration)}")
    
    if len(norm_reduction) > 0:
        converged = norm_reduction[-1] < 1e-10
        print(f"  Final gradient norm reduction: {norm_reduction[-1]:.2e}")
        print(f"  Converged: {'Yes' if converged else 'No'}")
        
        if converged:
            converged_idx = np.where(norm_reduction < 1e-10)[0]
            if len(converged_idx) > 0:
                print(f"  Convergence achieved at iteration: {iteration[converged_idx[0]]}")
    
    print(f"\nFinal Jb/Jo ratio: {Jb[-1]/Jo[-1]:.4f}")
    print("="*70 + "\n")


def main():
    """
    Main function to parse log file and create visualizations.
    """
    # Path to your log file
    log_file = '/discover/nobackup/mabdiosk/JEDI_practicals/live_demo/var/outputs/log_3denvar.txt'
    
    # Parse the log file
    print(f"Parsing log file: {log_file}")
    data = parse_variational_log(log_file)
    
    # Print summary statistics
    print_summary(data)
    
    # Create plots
    #plot_cost_function_convergence(data, output_file='./cost_function_convergence_3dvar_IB.png')
    plot_cost_function_convergence(data, output_file='./cost_function_convergence_3denvar.png')


if __name__ == '__main__':
    main()
