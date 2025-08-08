import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class DataVisualizer:
    """Data visualization component for geopolitical market analysis"""
    
    def __init__(self):
        self.color_scheme = {
            'positive': '#2ca02c',
            'negative': '#d62728',
            'neutral': '#ff7f0e',
            'risk_high': '#d62728',
            'risk_medium': '#ff7f0e',
            'risk_low': '#2ca02c'
        }
    
    def create_sentiment_chart(self, sentiment_data: Dict[str, Any]) -> go.Figure:
        """Create sentiment analysis chart"""
        if not sentiment_data:
            return self._create_empty_chart("No sentiment data available")
        
        # Create sentiment distribution
        labels = ['Positive', 'Negative', 'Neutral']
        values = [
            sentiment_data.get('positive_count', 0),
            sentiment_data.get('negative_count', 0),
            sentiment_data.get('neutral_count', 0)
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker_colors=['#2ca02c', '#d62728', '#ff7f0e']
        )])
        
        fig.update_layout(
            title="News Sentiment Distribution",
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_market_performance_chart(self, market_data: List[Dict[str, Any]]) -> go.Figure:
        """Create market performance chart"""
        if not market_data:
            return self._create_empty_chart("No market data available")
        
        df = pd.DataFrame(market_data)
        
        # Group by sector and calculate average performance
        sector_performance = df.groupby('sector')['change'].mean().reset_index()
        
        fig = px.bar(
            sector_performance,
            x='sector',
            y='change',
            color='change',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Market Performance by Sector"
        )
        
        fig.update_layout(
            xaxis_title="Sector",
            yaxis_title="Average Change (%)",
            height=400
        )
        
        return fig
    
    def create_risk_assessment_chart(self, risk_data: List[Dict[str, Any]]) -> go.Figure:
        """Create risk assessment visualization"""
        if not risk_data:
            return self._create_empty_chart("No risk data available")
        
        df = pd.DataFrame(risk_data)
        
        # Create bubble chart
        fig = px.scatter(
            df,
            x='Region',
            y='Risk Score',
            size='Risk Score',
            color='Risk Level',
            color_discrete_map={
                'High': self.color_scheme['risk_high'],
                'Medium': self.color_scheme['risk_medium'],
                'Low': self.color_scheme['risk_low']
            },
            title="Geopolitical Risk Assessment by Region"
        )
        
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Risk Score",
            height=500
        )
        
        return fig
    
    def create_market_impact_chart(self, impact_data: Dict[str, Any]) -> go.Figure:
        """Create market impact visualization"""
        if not impact_data or 'sector_impacts' not in impact_data:
            return self._create_empty_chart("No impact data available")
        
        sector_impacts = impact_data['sector_impacts']
        
        sectors = list(sector_impacts.keys())
        impact_scores = [impact['impact_score'] for impact in sector_impacts.values()]
        volatility = [impact['volatility_prediction'] for impact in sector_impacts.values()]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=sectors,
            y=impact_scores,
            mode='markers',
            marker=dict(
                size=volatility,
                color=impact_scores,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Impact Score")
            ),
            text=[f"Volatility: {v:.2f}" for v in volatility],
            hovertemplate="<b>%{x}</b><br>Impact: %{y:.2f}<br>Volatility: %{text}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Market Impact vs Volatility by Sector",
            xaxis_title="Sector",
            yaxis_title="Impact Score",
            height=500
        )
        
        return fig
    
    def create_news_timeline_chart(self, news_data: List[Dict[str, Any]]) -> go.Figure:
        """Create news timeline visualization"""
        if not news_data:
            return self._create_empty_chart("No news data available")
        
        # Prepare data for timeline
        timeline_data = []
        for news in news_data:
            try:
                # Parse timestamp
                if 'published_at' in news:
                    timestamp = pd.to_datetime(news['published_at'])
                else:
                    timestamp = datetime.now()
                
                timeline_data.append({
                    'timestamp': timestamp,
                    'title': news.get('title', 'Unknown'),
                    'region': news.get('region', 'Unknown'),
                    'source': news.get('source', 'Unknown'),
                    'sentiment': news.get('sentiment', 0)
                })
            except Exception as e:
                print(f"Error processing news item: {e}")
        
        if not timeline_data:
            return self._create_empty_chart("No valid news data available")
        
        df = pd.DataFrame(timeline_data)
        
        # Create timeline chart
        fig = px.scatter(
            df,
            x='timestamp',
            y='sentiment',
            color='region',
            size=abs(df['sentiment']),
            hover_data=['title', 'source'],
            title="News Timeline with Sentiment"
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Sentiment Score",
            height=400
        )
        
        return fig
    
    def create_geopolitical_heatmap(self, news_data: List[Dict[str, Any]], regions: List[str]) -> go.Figure:
        """Create geopolitical activity heatmap"""
        if not news_data or not regions:
            return self._create_empty_chart("No data available for heatmap")
        
        # Count news by region and calculate average sentiment
        region_data = {}
        for region in regions:
            region_news = [news for news in news_data if news.get('region') == region]
            if region_news:
                sentiments = [news.get('sentiment', 0) for news in region_news]
                region_data[region] = {
                    'count': len(region_news),
                    'avg_sentiment': np.mean(sentiments),
                    'activity_level': len(region_news) / max(len(news_data), 1)
                }
            else:
                region_data[region] = {
                    'count': 0,
                    'avg_sentiment': 0,
                    'activity_level': 0
                }
        
        # Create heatmap data
        regions_list = list(region_data.keys())
        activity_levels = [region_data[r]['activity_level'] for r in regions_list]
        sentiment_levels = [region_data[r]['avg_sentiment'] for r in regions_list]
        
        fig = go.Figure(data=go.Heatmap(
            z=[activity_levels, sentiment_levels],
            x=regions_list,
            y=['Activity Level', 'Sentiment'],
            colorscale='RdYlBu',
            zmid=0
        ))
        
        fig.update_layout(
            title="Geopolitical Activity Heatmap",
            xaxis_title="Region",
            yaxis_title="Metric",
            height=400
        )
        
        return fig
    
    def create_comprehensive_dashboard(self, news_data: List[Dict[str, Any]], 
                                    market_data: List[Dict[str, Any]], 
                                    risk_data: List[Dict[str, Any]]) -> go.Figure:
        """Create a comprehensive dashboard with multiple charts"""
        
        # Create subplots
        fig = sp.make_subplots(
            rows=2, cols=2,
            subplot_titles=('Market Performance', 'Risk Assessment', 
                          'News Sentiment', 'Geopolitical Activity'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "heatmap"}]]
        )
        
        # Market Performance
        if market_data:
            df_market = pd.DataFrame(market_data)
            sector_perf = df_market.groupby('sector')['change'].mean()
            
            fig.add_trace(
                go.Bar(x=sector_perf.index, y=sector_perf.values, name="Market Performance"),
                row=1, col=1
            )
        
        # Risk Assessment
        if risk_data:
            df_risk = pd.DataFrame(risk_data)
            fig.add_trace(
                go.Scatter(x=df_risk['Region'], y=df_risk['Risk Score'], 
                          mode='markers', name="Risk Assessment"),
                row=1, col=2
            )
        
        # News Sentiment
        if news_data:
            # Calculate sentiment distribution
            sentiments = [news.get('sentiment', 0) for news in news_data]
            positive = sum(1 for s in sentiments if s > 0)
            negative = sum(1 for s in sentiments if s < 0)
            neutral = sum(1 for s in sentiments if s == 0)
            
            fig.add_trace(
                go.Pie(labels=['Positive', 'Negative', 'Neutral'], 
                      values=[positive, negative, neutral], name="Sentiment"),
                row=2, col=1
            )
        
        # Geopolitical Activity
        if news_data:
            # Count news by region
            regions = {}
            for news in news_data:
                region = news.get('region', 'Unknown')
                regions[region] = regions.get(region, 0) + 1
            
            fig.add_trace(
                go.Heatmap(z=[[list(regions.values())]], 
                          x=list(regions.keys()), 
                          y=['Activity'], name="Activity"),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Geopolitical Market Analysis Dashboard",
            height=800,
            showlegend=False
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        return fig
    
    def create_interactive_map(self, risk_data: List[Dict[str, Any]]) -> go.Figure:
        """Create an interactive world map showing geopolitical risks"""
        # This would integrate with a world map visualization
        # For now, return a placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="Interactive World Map - Geopolitical Risk Assessment",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title="Geopolitical Risk World Map",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        return fig
