import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'plots')

METRIC_COLS = [
    'path_length',
    'visited',
    'max_fringe_size',
    'total_iterations',
    'inner_iterations',
    'outer_iterations',
    'runtime_s',
    'memory_bytes',
]


def load_results(run_id: str | None = None) -> tuple[pd.DataFrame, str]:
    results_dir = os.path.abspath(RESULTS_DIR)
    all_files = sorted(
        f
        for f in os.listdir(results_dir)
        if f.endswith('.csv') and not f.startswith('results_')
    )

    if run_id:
        csv_files = [f for f in all_files if f.startswith(run_id)]
        if not csv_files:
            print(f'No CSV files found for run ID {run_id!r} in {results_dir}')
            return pd.DataFrame(), ''
    else:
        csv_files = all_files
        if not csv_files:
            print(f'No CSV files found in {results_dir}')
            return pd.DataFrame(), ''

    frames = []
    run_ids = []
    for filename in csv_files:
        print(f'Loading {filename}')
        frames.append(pd.read_csv(os.path.join(results_dir, filename)))
        run_ids.append(filename.split('_')[0])

    return pd.concat(frames, ignore_index=True), '_'.join(dict.fromkeys(run_ids))


def _compute_stats(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    present = [c for c in metrics if c in df.columns and df[c].notna().any()]
    stats = df.groupby(['algorithm', 'size'])[present].agg(['mean', 'std']).round(4)
    stats.columns = [f'{metric}_{agg}' for metric, agg in stats.columns]
    return stats.reset_index()


def _print_stats(df: pd.DataFrame, label: str, metrics: list[str]) -> None:
    present = [c for c in metrics if c in df.columns and df[c].notna().any()]
    stats = df.groupby(['algorithm', 'size'])[present].agg(['mean', 'std']).round(4)
    print(f'\n=== {label} ===\n')
    print(stats.to_string())


def _write_csv(pf_stats: pd.DataFrame, mdp_stats: pd.DataFrame, run_id: str) -> None:
    results_dir = os.path.abspath(RESULTS_DIR)
    filepath = os.path.join(results_dir, f'results_{run_id}.csv')

    pf_stats.insert(0, 'type', 'pathfinding')
    mdp_stats.insert(0, 'type', 'mdp')

    pd.concat([pf_stats, mdp_stats], ignore_index=True).to_csv(filepath, index=False)
    print(f'\nResults written to {filepath}')


_METRIC_LABELS = {
    'path_length': 'Path length',
    'visited': 'Cells visited',
    'max_fringe_size': 'Max frontier size',
    'total_iterations': 'Total iterations',
    'inner_iterations': 'Inner iterations (policy eval)',
    'outer_iterations': 'Outer iterations (policy improve)',
    'runtime_ms': 'Runtime (ms)',
    'runtime_s': 'Runtime (s)',
    'memory_kb': 'Memory (KB)',
}


def _plot_pf_metric(
    pf: pd.DataFrame, sizes: list[int], metric: str, run_id: str
) -> None:
    label = _METRIC_LABELS.get(metric, metric)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharey=True)
    fig.suptitle(f'Pathfinding - {label} by Algorithm and Maze Size')

    for ax, size in zip(axes.flat, sizes):
        sub = pf[pf['size'] == size].groupby('algorithm')[metric].agg(['mean', 'std'])
        algorithms = sub.index.tolist()
        means = sub['mean'].tolist()
        stds = sub['std'].fillna(0).tolist()

        ax.errorbar(
            algorithms,
            means,
            yerr=stds,
            fmt='o',
            capsize=5,
            capthick=1.5,
            elinewidth=1.5,
            markersize=6,
            ecolor='grey',
            label='Mean ± Std. dev.',
        )
        ax.set_title(f'Size {size}×{size}')
        ax.set_xlabel('Algorithm')
        ax.set_ylabel(label)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    legend_ax = axes.flat[-1]
    legend_ax.set_visible(True)
    legend_ax.axis('off')
    handles, labels = axes.flat[0].get_legend_handles_labels()
    legend_ax.legend(handles=handles, labels=labels, loc='center', frameon=True)

    plt.tight_layout()
    plots_dir = os.path.abspath(PLOTS_DIR)
    os.makedirs(plots_dir, exist_ok=True)
    fig.savefig(os.path.join(plots_dir, f'pathfinding-{metric}-{run_id}.png'))
    plt.close(fig)


def _plot_mdp_metric(
    mdp: pd.DataFrame, sizes: list[int], metric: str, run_id: str
) -> None:
    label = _METRIC_LABELS.get(metric, metric)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharey=True)
    fig.suptitle(f'MDP - {label} by Algorithm and Maze Size')

    for ax, size in zip(axes.flat, sizes):
        sub = mdp[mdp['size'] == size].groupby('algorithm')[metric].agg(['mean', 'std'])
        algorithms = sub.index.tolist()
        means = sub['mean'].tolist()
        stds = sub['std'].fillna(0).tolist()

        ax.errorbar(
            algorithms,
            means,
            yerr=stds,
            fmt='o',
            capsize=5,
            capthick=1.5,
            elinewidth=1.5,
            markersize=6,
            ecolor='grey',
            label='Mean ± Std. dev.',
        )
        ax.margins(x=0.5)
        ax.set_title(f'Size {size}×{size}')
        ax.set_xlabel('Algorithm')
        ax.set_ylabel(label)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    legend_ax = axes.flat[-1]
    legend_ax.set_visible(True)
    legend_ax.axis('off')
    handles, labels = axes.flat[0].get_legend_handles_labels()
    legend_ax.legend(handles=handles, labels=labels, loc='center', frameon=True)

    plt.tight_layout()
    plots_dir = os.path.abspath(PLOTS_DIR)
    os.makedirs(plots_dir, exist_ok=True)
    fig.savefig(os.path.join(plots_dir, f'mdp-{metric}-{run_id}.png'))
    plt.close(fig)


def _plot_mdp_iterations(mdp: pd.DataFrame, sizes: list[int], run_id: str) -> None:
    series = [
        ('VI Total', 'Value Iteration', 'total_iterations'),
        ('PI Total', 'Policy Iteration', 'total_iterations'),
        ('PI Outer', 'Policy Iteration', 'outer_iterations'),
        ('PI Inner', 'Policy Iteration', 'inner_iterations'),
    ]
    x_labels = [label for label, _, _ in series]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharey=True)
    fig.suptitle('MDP - Iterations by Algorithm and Maze Size')

    for ax, size in zip(axes.flat, sizes):
        means, stds = [], []
        for _, algo, col in series:
            sub = mdp[(mdp['size'] == size) & (mdp['algorithm'] == algo)][col]
            means.append(sub.mean())
            stds.append(sub.std(ddof=1) if len(sub) > 1 else 0)

        ax.errorbar(
            x_labels,
            means,
            yerr=stds,
            fmt='o',
            capsize=5,
            capthick=1.5,
            elinewidth=1.5,
            markersize=6,
            ecolor='grey',
            label='Mean ± Std. dev.',
        )
        ax.margins(x=0.3)
        ax.set_title(f'Size {size}×{size}')
        ax.set_xlabel('Scope')
        ax.set_ylabel('Iterations')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    legend_ax = axes.flat[-1]
    legend_ax.set_visible(True)
    legend_ax.axis('off')
    handles, labels = axes.flat[0].get_legend_handles_labels()
    legend_ax.legend(handles=handles, labels=labels, loc='center', frameon=True)

    plt.tight_layout()
    plots_dir = os.path.abspath(PLOTS_DIR)
    os.makedirs(plots_dir, exist_ok=True)
    fig.savefig(os.path.join(plots_dir, f'mdp-iterations-{run_id}.png'))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--runid', type=str, default=None, help='Run ID prefix to filter CSV files'
    )
    args = parser.parse_args()

    df, run_id = load_results(args.runid)
    if df.empty:
        return

    print(f'\nLoaded {len(df)} rows\n')

    pf = df[df['type'] == 'pathfinding']
    mdp = df[df['type'] == 'mdp']

    pf_metrics = [
        'path_length',
        'visited',
        'max_fringe_size',
        'runtime_ms',
        'memory_kb',
    ]
    mdp_metrics = [
        'path_length',
        'runtime_s',
        'memory_kb',
    ]

    if not pf.empty:
        pf = pf.copy()
        pf['runtime_ms'] = pf['runtime_s'] * 1000
        pf['memory_kb'] = pf['memory_bytes'] / 1024
        _print_stats(pf, 'Pathfinding — mean ± std per algorithm × size', pf_metrics)

    if not mdp.empty:
        mdp = mdp.copy()
        mdp['memory_kb'] = mdp['memory_bytes'] / 1024
        _print_stats(mdp, 'MDP — mean ± std per algorithm × size', mdp_metrics)

    pf_stats = _compute_stats(pf, pf_metrics) if not pf.empty else pd.DataFrame()
    mdp_stats = _compute_stats(mdp, mdp_metrics) if not mdp.empty else pd.DataFrame()

    if not pf_stats.empty or not mdp_stats.empty:
        _write_csv(pf_stats, mdp_stats, run_id)

    if not pf.empty:
        plot_sizes = sorted(pf['size'].unique())[:5]
        for metric in pf_metrics:
            _plot_pf_metric(pf, plot_sizes, metric, run_id)

    if not mdp.empty:
        plot_sizes = sorted(mdp['size'].unique())[:5]
        for metric in mdp_metrics:
            _plot_mdp_metric(mdp, plot_sizes, metric, run_id)
        _plot_mdp_iterations(mdp, plot_sizes, run_id)


if __name__ == '__main__':
    main()
