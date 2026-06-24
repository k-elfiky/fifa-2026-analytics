import pandas as pd
import numpy as np
file_path = 'fifa_world_cup_2026_player_performance.csv'
class AdvancedTournamentEngine:
    """
    Advanced Statistical Processing Engine for the FIFA World Cup 2026 dataset.
    Handles vectorized data cleaning, advanced feature engineering, metric normalization, 
    and multi-dimensional cohort profiling.
    """
    def __init__(self, file_path: str = file_path):
        try:
            self.df = pd.read_csv(file_path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to read dataset from path: {file_path}. Error: {e}")
        self._execute_pipeline()

    def _execute_pipeline(self):
        """Executes full mathematical processing and feature engineering pipeline."""
        # Clean dates safely using pandas native datetime structures
        self.df['match_date'] = pd.to_datetime(self.df['match_date'])
        
        # 1. Continuous Rate Metrics via Vectorized NumPy divisions (Handling division by zero)
        mins = self.df['minutes_played'].to_numpy()
        self.df['expected_contributions_per_90'] = np.where(
            mins > 0,
            ((self.df['expected_goals_xg'] + self.df['expected_assists_xa']) / mins) * 90,
            0.0
        )
        
        # 2. Work-Rate Index (Combining sprint profile vectors with physical outputs)
        self.df['work_rate_index'] = (
            (self.df['distance_covered_km'] * 0.4) + 
            (self.df['sprint_distance_km'] * 0.4) + 
            (self.df['accelerations'] * 0.1)
        )
        
        # 3. Positional Standardizations (Z-Score Normalization within Specific Playing Roles)
        # Avoids penalizing defenders for low goals or strikers for low tackles.
        self.df['z_performance_score'] = self.df.groupby('position')['player_rating'].transform(
            lambda x: (x - x.mean()) / (x.std() + 1e-9)
        )

    def compute_mvp_cohort(self, min_minutes: int = 60, top_n: int = 15) -> pd.DataFrame:
        """
        Calculates absolute tournament value using grouped aggregate metrics and financial evaluations.
        """
        filtered_df = self.df[self.df['total_minutes_tournament'] >= min_minutes]
        
        cohort = filtered_df.groupby(['player_id', 'player_name', 'team', 'position']).agg(
            avg_rating=('tournament_rating', 'mean'),
            peak_z_score=('z_performance_score', 'max'),
            goals=('goals', 'sum'),
            assists=('assists', 'sum'),
            total_xg=('expected_goals_xg', 'sum'),
            market_value=('market_value_eur', 'first')
        ).reset_index()
        
        # Performance vs Market Value Efficiency Metric
        cohort['value_efficiency_index'] = (cohort['avg_rating'] / (cohort['market_value'] + 1e-9)) * 1_000_000
        
        return cohort.sort_values(by='avg_rating', ascending=False).head(top_n)

    def segment_tactical_archetypes(self) -> pd.DataFrame:
        """
        Generates tactical archetype matrix profiles based on operational biometric indices and 
        play-style drivers using custom matrix scaling.
        """
        archetypes = self.df.groupby('position').agg(
            stamina=('stamina_score', 'mean'),
            creativity=('creativity_score', 'mean'),
            consistency=('consistency_score', 'mean'),
            pressure_resistance=('pressure_resistance', 'mean'),
            top_speed=('top_speed_kmh', 'max'),
            avg_distance=('distance_covered_km', 'mean')
        ).reset_index()
        return archetypes

    def get_efficiency_outliers(self) -> pd.DataFrame:
        """
        Identifies goal-scoring conversion efficiency outliers by subtracting expected goals (xG) 
        from actual tournament goals scored.
        """
        player_stats = self.df.groupby(['player_name', 'team']).agg(
            actual_goals=('goals', 'sum'),
            expected_goals=('expected_goals_xg', 'sum'),
            minutes=('minutes_played', 'sum')
        ).reset_index()
        
        player_stats['xg_delta'] = player_stats['actual_goals'] - player_stats['expected_goals']
        return player_stats.sort_values(by='xg_delta', ascending=False)