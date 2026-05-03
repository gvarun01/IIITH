"""
Q3: Sandpile Model (BTW Model)
Roll Number: 203101108
Course: UAS Spring'26

Parameters:
- Lattice Size L = ((roll % 7) + 1) × 10 = 10
- Grid: 10 × 10
- Avalanche Threshold = (roll % 5) + 3 = 6
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# PARAMETERS
# ============================================================================
ROLL_NUMBER = 203101108

L = ((ROLL_NUMBER % 7) + 1) * 10  # = 10
THRESHOLD = (ROLL_NUMBER % 5) + 3  # = 6

print("=" * 70)
print("Q3: SANDPILE MODEL (BTW MODEL)")
print("=" * 70)
print(f"\nRoll Number: {ROLL_NUMBER}")
print(f"Roll Number % 7 = {ROLL_NUMBER % 7}")
print(f"Roll Number % 5 = {ROLL_NUMBER % 5}")
print(f"\nParameters:")
print(f"  Lattice Size L = {L}")
print(f"  Grid: {L} × {L}")
print(f"  Avalanche Threshold z_c = {THRESHOLD}")

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def topple_step(grid, threshold):
    """
    Perform one parallel toppling sweep.
    All sites with z >= threshold topple simultaneously.
    
    Uses OPEN boundary conditions:
    - Grains going outside the grid are lost
    
    Returns:
        new_grid: Updated grid after toppling
        num_toppled: Number of sites that toppled
    """
    L = grid.shape[0]
    
    # Find unstable sites
    unstable = grid >= threshold
    num_toppled = np.sum(unstable)
    
    if num_toppled == 0:
        return grid.copy(), 0
    
    # Create new grid
    new_grid = grid.copy()
    
    # Each unstable site loses 4 grains
    new_grid[unstable] -= 4
    
    # Distribute grains to neighbors (open boundary - grains at edge are lost)
    # Top neighbor (i-1, j)
    new_grid[1:, :] += unstable[:-1, :].astype(int)
    # Bottom neighbor (i+1, j)
    new_grid[:-1, :] += unstable[1:, :].astype(int)
    # Left neighbor (i, j-1)
    new_grid[:, 1:] += unstable[:, :-1].astype(int)
    # Right neighbor (i, j+1)
    new_grid[:, :-1] += unstable[:, 1:].astype(int)
    
    return new_grid, num_toppled


def relax(grid, threshold, max_steps=10000):
    """
    Run the sandpile until it reaches a stable state.
    
    Returns:
        final_grid: Stable configuration
        total_steps: Number of toppling sweeps performed
        history: List of (step, num_toppled) tuples
    """
    current_grid = grid.copy()
    history = []
    
    for step in range(max_steps):
        current_grid, num_toppled = topple_step(current_grid, threshold)
        history.append((step, num_toppled))
        
        if num_toppled == 0:
            break
    
    return current_grid, step, history


def plot_sandpile(grid, threshold, title, filename=None, show_values=True, 
                  mark_center=False, center=None):
    """
    Plot the sandpile configuration with a nice colormap.
    """
    L = grid.shape[0]
    fig, ax = plt.subplots(figsize=(8, 7))
    
    # Plot
    im = ax.imshow(grid, cmap='YlOrRd', vmin=0, vmax=threshold, interpolation='nearest')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, label='Height z(i,j)')
    cbar.set_ticks(range(threshold + 1))
    
    # Add grid lines
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Show values in cells if grid is small enough
    if show_values and grid.shape[0] <= 15:
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                val = grid[i, j]
                color = 'white' if val > threshold/2 else 'black'
                ax.text(j, i, str(val), ha='center', va='center', 
                       fontsize=8, color=color, fontweight='bold')
    
    # Mark center if requested
    if mark_center and center is not None:
        ax.plot(center, center, 'g*', markersize=20, markeredgecolor='black', markeredgewidth=1.5)
    
    ax.set_xlabel('Column j', fontsize=11)
    ax.set_ylabel('Row i', fontsize=11)
    ax.set_title(title, fontsize=12)
    
    # Set ticks
    ax.set_xticks(range(grid.shape[1]))
    ax.set_yticks(range(grid.shape[0]))
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Figure saved: {filename}")
    
    plt.close()
    
    return fig


# ============================================================================
# PART 1: INITIAL RELAXATION
# ============================================================================
print("\n" + "=" * 70)
print("PART 1: INITIAL RELAXATION")
print("=" * 70)

# Initialize all sites at threshold
initial_grid = np.full((L, L), THRESHOLD, dtype=int)

print(f"\nInitial Configuration:")
print(f"  All sites set to z = {THRESHOLD} (threshold)")
print(f"  Grid size: {L} × {L}")
print(f"  Total grains: {np.sum(initial_grid)}")
print(f"\nStarting relaxation...")

# Run relaxation
final_grid, total_steps, history = relax(initial_grid, THRESHOLD)

print(f"\nRelaxation Complete!")
print(f"  Time steps to stabilize: {total_steps}")
print(f"  Total grains remaining: {np.sum(final_grid)}")
print(f"  Grains lost at boundary: {np.sum(initial_grid) - np.sum(final_grid)}")
print(f"  Max height in final state: {np.max(final_grid)}")
print(f"  Min height in final state: {np.min(final_grid)}")

# Plot final state after initial relaxation
plot_sandpile(final_grid, THRESHOLD, 
              f'Final Stable State After Initial Relaxation\n(Started from all sites at z = {THRESHOLD}, L = {L}×{L})',
              'figures/initial_relaxation.png')

print("\n" + "-" * 70)
print("INTERPRETATION OF INITIAL RELAXATION:")
print("-" * 70)
print(f"""
1. Starting state: All {L*L} sites at z = {THRESHOLD} (threshold), totaling {L*L*THRESHOLD} grains.

2. Massive avalanche: Since every site starts at threshold, the entire system 
   is unstable. A massive cascade of topplings occurs.

3. Grain loss: {np.sum(initial_grid) - np.sum(final_grid)} grains were lost at the open boundaries.

4. Final pattern: The stable configuration shows:
   - Lower values near the edges (grains have escaped)
   - Higher values toward the center (harder for grains to escape)
   - All values strictly below threshold (z < {THRESHOLD})

5. Self-organized criticality: The system has naturally evolved to a critical
   state where it's stable but sensitive to small perturbations.
""")

# ============================================================================
# PART 2: PERTURBATION AND EVOLUTION
# ============================================================================
print("\n" + "=" * 70)
print("PART 2: PERTURBATION AND EVOLUTION")
print("=" * 70)

# Start from the relaxed state
perturbed_grid = final_grid.copy()

# Add 1 grain at the center
center = L // 2
print(f"\nAdding 1 grain at center position ({center}, {center})")
print(f"Height before: {perturbed_grid[center, center]}")

perturbed_grid[center, center] += 1

print(f"Height after: {perturbed_grid[center, center]}")
print(f"Threshold: {THRESHOLD}")
print(f"Site is unstable: {perturbed_grid[center, center] >= THRESHOLD}")

# Record states at specific time steps
states = {}
current_grid = perturbed_grid.copy()

# t = 0: Just after perturbation
states[0] = current_grid.copy()

# Run simulation and record at various times
max_time = 100

print(f"\n{'Time':>6} | {'Sites Toppled':>14} | {'Max Height':>10}")
print("-" * 40)

total_toppled = 0
for t in range(1, max_time + 1):
    current_grid, num_toppled = topple_step(current_grid, THRESHOLD)
    total_toppled += num_toppled
    
    # Store state
    states[t] = current_grid.copy()
    
    if t <= 25 or num_toppled == 0:
        print(f"{t:>6} | {num_toppled:>14} | {np.max(current_grid):>10}")
    
    if num_toppled == 0:
        print(f"\nSystem stabilized at t = {t}")
        break

final_time = t

print(f"\nTotal sites toppled during avalanche: {total_toppled}")
print(f"Time to stabilize: {final_time} steps")

# Determine which time points we actually have
# We'll use t=0, and evenly spaced points, plus final
if final_time >= 20:
    time_points = [0, 10, 20, final_time]
elif final_time >= 10:
    time_points = [0, final_time // 2, 10, final_time]
elif final_time >= 3:
    time_points = [0, 1, final_time // 2, final_time]
else:
    time_points = [0, 1, max(2, final_time-1), final_time]

# Remove duplicates and sort
time_points = sorted(list(set(time_points)))
# Ensure we have exactly 4 points
while len(time_points) < 4:
    for i in range(1, final_time):
        if i not in time_points:
            time_points.append(i)
            time_points = sorted(time_points)
            break
time_points = time_points[:4]

print(f"\nTime points for visualization: {time_points}")

# Plot all four states in a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for idx, (ax, t) in enumerate(zip(axes.flat, time_points)):
    grid = states[t]
    
    if t == final_time:
        title = f't = {t} (Final Stable State)'
    elif t == 0:
        title = f't = {t} (Just After Perturbation)'
    else:
        title = f't = {t}'
    
    im = ax.imshow(grid, cmap='YlOrRd', vmin=0, vmax=THRESHOLD, interpolation='nearest')
    
    # Add grid lines
    ax.set_xticks(np.arange(-0.5, L, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, L, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Show values
    for i in range(L):
        for j in range(L):
            val = grid[i, j]
            color = 'white' if val > THRESHOLD/2 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=7, color=color, fontweight='bold')
    
    # Mark center at t=0
    if t == 0:
        ax.plot(center, center, 'g*', markersize=15, markeredgecolor='black', markeredgewidth=1)
    
    ax.set_xlabel('Column j')
    ax.set_ylabel('Row i')
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xticks(range(L))
    ax.set_yticks(range(L))

# Add colorbar
fig.subplots_adjust(right=0.9)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax, label='Height z(i,j)')
cbar.set_ticks(range(THRESHOLD + 1))

fig.suptitle(f'Sandpile Evolution After Center Perturbation\n(L = {L}×{L}, Threshold = {THRESHOLD})', 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('figures/perturbation_evolution.png', dpi=150, bbox_inches='tight')
print("\nFigure saved: figures/perturbation_evolution.png")
plt.close()

# Save individual figures
for t in time_points:
    grid = states[t]
    
    if t == final_time:
        title = f'Final Stable State (t = {t})'
        fname = 'figures/perturbation_final.png'
    elif t == 0:
        title = f'State at t = {t} (Just After Perturbation)'
        fname = 'figures/perturbation_t0.png'
    else:
        title = f'State at t = {t}'
        fname = f'figures/perturbation_t{t}.png'
    
    plot_sandpile(grid, THRESHOLD, 
                  f'{title}\n(After Center Perturbation, L = {L}×{L})',
                  fname, mark_center=(t==0), center=center)

# ============================================================================
# DIFFERENCE MAP
# ============================================================================
print("\n" + "=" * 70)
print("DIFFERENCE MAP ANALYSIS")
print("=" * 70)

diff_grid = states[final_time] - final_grid

fig, ax = plt.subplots(figsize=(8, 7))

max_diff = max(abs(diff_grid.min()), abs(diff_grid.max()), 1)

im = ax.imshow(diff_grid, cmap='RdBu_r', vmin=-max_diff, vmax=max_diff, interpolation='nearest')

ax.set_xticks(np.arange(-0.5, L, 1), minor=True)
ax.set_yticks(np.arange(-0.5, L, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

for i in range(L):
    for j in range(L):
        val = diff_grid[i, j]
        if val != 0:
            color = 'white' if abs(val) > max_diff/2 else 'black'
            ax.text(j, i, f'{val:+d}', ha='center', va='center', 
                   fontsize=8, color=color, fontweight='bold')

plt.colorbar(im, ax=ax, label='Change in Height')
ax.set_xlabel('Column j')
ax.set_ylabel('Row i')
ax.set_title('Difference Map: Final State After Perturbation - Initial Stable State\n(Red = gained grains, Blue = lost grains)')
ax.set_xticks(range(L))
ax.set_yticks(range(L))

plt.tight_layout()
plt.savefig('figures/difference_map.png', dpi=150, bbox_inches='tight')
print("Figure saved: figures/difference_map.png")
plt.close()

print(f"\nTotal change in grains: {np.sum(diff_grid)}")
print("(Negative means grains were lost to boundary)")

# ============================================================================
# INTERPRETATION
# ============================================================================
print("\n" + "-" * 70)
print("INTERPRETATION OF PERTURBATION EVOLUTION:")
print("-" * 70)
print(f"""
Figure Analysis:

**t = 0 (Just After Perturbation):**
- One grain added at center position ({center}, {center})
- The center site height increased from {final_grid[center, center]} to {final_grid[center, center] + 1}
- Unstable: {final_grid[center, center] + 1 >= THRESHOLD}
- The green star marks the perturbation location

**Evolution (t = 1 to {final_time}):**
- The avalanche propagates outward from the center
- Sites redistribute their grains to neighbors
- Grains reaching the boundary fall off (open boundary)

**Final State (t = {final_time}):**
- System has returned to a stable configuration
- All heights are below threshold (z < {THRESHOLD})
- Total of {total_toppled} toppling events occurred
- {-np.sum(diff_grid)} grain(s) lost to boundary

Key Physics:

1. SENSITIVITY TO PERTURBATION: A single grain can trigger a cascade.

2. SPATIAL PROPAGATION: The avalanche spreads outward from the 
   perturbation site in a wave-like manner.

3. BOUNDARY EFFECTS: Grains are lost at the open boundaries, 
   allowing the system to eventually stabilize.

4. SELF-ORGANIZED CRITICALITY: The system naturally returns to a 
   critical state after the perturbation - ready to avalanche again 
   with the next grain drop.
""")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
Parameters:
  - Roll Number: {ROLL_NUMBER}
  - Lattice Size: {L} × {L}
  - Avalanche Threshold: {THRESHOLD}
  - Boundary Condition: Open (grains lost at edges)

Results:
  - Initial Relaxation: {total_steps} steps to stabilize from all-{THRESHOLD} state
  - Perturbation Response: {final_time} steps to stabilize after +1 grain at center
  - Total Avalanche Size: {total_toppled} toppling events

Figures Generated:
  1. figures/initial_relaxation.png - Stable state after initial relaxation
  2. figures/perturbation_evolution.png - 2×2 grid of time evolution
  3. figures/perturbation_t0.png - State just after perturbation
  4. figures/perturbation_t*.png - Intermediate states
  5. figures/perturbation_final.png - Final stable state
  6. figures/difference_map.png - Change due to perturbation
""")

print("=" * 70)
print("EXECUTION COMPLETE")
print("=" * 70)
