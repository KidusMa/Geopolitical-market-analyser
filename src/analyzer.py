import openai
import os
from typing import List, Dict, Any, Optional
from textblob import TextBlob
import pandas as pd
import numpy as np
from datetime import datetime
import json

class GeopoliticalAnalyzer:
    """AI-powered geopolitical analysis engine"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Analysis categories
        self.analysis_categories = [
            'political_stability', 'economic_impact', 'market_volatility',
            'trade_relations', 'diplomatic_tensions', 'regional_conflicts'
        ]
        
        # Sentiment analysis model
        self.sentiment_model = TextBlob
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text using TextBlob"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return 0.0
    
    def analyze_news_sentiment(self, news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment across multiple news articles"""
        if not news_data:
            return {}
        
        sentiments = []
        for news in news_data:
            sentiment = self.analyze_sentiment(news.get('content', '') + ' ' + news.get('title', ''))
            sentiments.append(sentiment)
        
        return {
            'average_sentiment': np.mean(sentiments),
            'sentiment_std': np.std(sentiments),
            'positive_count': sum(1 for s in sentiments if s > 0),
            'negative_count': sum(1 for s in sentiments if s < 0),
            'neutral_count': sum(1 for s in sentiments if s == 0),
            'total_articles': len(sentiments)
        }
    
    def generate_ai_analysis(self, news_data: List[Dict[str, Any]], market_data: List[Dict[str, Any]]) -> str:
        """Generate AI-powered geopolitical analysis"""
        try:
            # Prepare context for AI analysis
            context = self._prepare_analysis_context(news_data, market_data)
            
            # Generate analysis using OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a geopolitical market analyst expert. Analyze the provided news and market data to provide insights on:
                        1. Key geopolitical developments and their market implications
                        2. Potential risks and opportunities for investors
                        3. Sector-specific impacts
                        4. Regional stability assessment
                        5. Investment recommendations
                        
                        Provide a comprehensive analysis in a clear, professional format."""
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze the following geopolitical and market data:\n\n{context}"
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating AI analysis: {e}")
            return self._generate_fallback_analysis(news_data, market_data)
    
    def _prepare_analysis_context(self, news_data: List[Dict[str, Any]], market_data: List[Dict[str, Any]]) -> str:
        """Prepare context for AI analysis"""
        context = "=== GEOPOLITICAL NEWS ===\n"
        
        for news in news_data[:5]:  # Top 5 news articles
            context += f"Title: {news.get('title', 'N/A')}\n"
            context += f"Summary: {news.get('summary', 'N/A')}\n"
            context += f"Region: {news.get('region', 'N/A')}\n"
            context += f"Source: {news.get('source', 'N/A')}\n\n"
        
        context += "=== MARKET DATA ===\n"
        for data in market_data[:10]:  # Top 10 market data points
            context += f"Symbol: {data.get('symbol', 'N/A')}\n"
            context += f"Sector: {data.get('sector', 'N/A')}\n"
            context += f"Price: {data.get('price', 'N/A')}\n"
            context += f"Change: {data.get('change', 'N/A')}\n\n"
        
        return context
    
    def _generate_fallback_analysis(self, news_data: List[Dict[str, Any]], market_data: List[Dict[str, Any]]) -> str:
        """Generate fallback analysis when AI is unavailable"""
        analysis = "=== GEOPOLITICAL MARKET ANALYSIS ===\n\n"
        
        # Analyze news sentiment
        sentiment_analysis = self.analyze_news_sentiment(news_data)
        
        analysis += f"Overall Market Sentiment: {sentiment_analysis.get('average_sentiment', 0):.2f}\n"
        analysis += f"Positive News Articles: {sentiment_analysis.get('positive_count', 0)}\n"
        analysis += f"Negative News Articles: {sentiment_analysis.get('negative_count', 0)}\n\n"
        
        # Analyze market performance by sector
        if market_data:
            sector_performance = {}
            for data in market_data:
                sector = data.get('sector', 'Unknown')
                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append(data.get('change', 0))
            
            analysis += "=== SECTOR PERFORMANCE ===\n"
            for sector, changes in sector_performance.items():
                avg_change = np.mean(changes)
                analysis += f"{sector}: {avg_change:.2%}\n"
        
        analysis += "\n=== KEY INSIGHTS ===\n"
        analysis += "• Monitor geopolitical developments in key regions\n"
        analysis += "• Consider sector-specific impacts of political events\n"
        analysis += "• Diversify investments to mitigate geopolitical risks\n"
        analysis += "• Stay informed about trade relations and policy changes\n"
        
        return analysis
    
    def assess_geopolitical_risk(self, region: str, news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess geopolitical risk for a specific region"""
        try:
            # Filter news for the specific region
            region_news = [news for news in news_data if news.get('region') == region]
            
            if not region_news:
                return {
                    'region': region,
                    'risk_score': 0.5,
                    'risk_level': 'Medium',
                    'confidence': 0.3,
                    'key_factors': ['Limited data available']
                }
            
            # Analyze sentiment for the region
            sentiment_analysis = self.analyze_news_sentiment(region_news)
            avg_sentiment = sentiment_analysis.get('average_sentiment', 0)
            
            # Calculate risk score (negative sentiment = higher risk)
            risk_score = max(0, min(1, 0.5 - avg_sentiment * 0.3))
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = 'High'
            elif risk_score > 0.4:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            # Identify key risk factors
            key_factors = self._identify_risk_factors(region_news)
            
            return {
                'region': region,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'confidence': min(1.0, len(region_news) / 10),  # More news = higher confidence
                'key_factors': key_factors,
                'sentiment': avg_sentiment
            }
            
        except Exception as e:
            print(f"Error assessing risk for {region}: {e}")
            return {
                'region': region,
                'risk_score': 0.5,
                'risk_level': 'Medium',
                'confidence': 0.0,
                'key_factors': ['Analysis error']
            }
    
    def _identify_risk_factors(self, news_data: List[Dict[str, Any]]) -> List[str]:
        """Identify key risk factors from news data"""
        risk_keywords = [
            'conflict', 'tension', 'sanctions', 'embargo', 'war',
            'crisis', 'instability', 'protest', 'unrest', 'violence'
        ]
        
        risk_factors = []
        for news in news_data:
            content = (news.get('title', '') + ' ' + news.get('content', '')).lower()
            for keyword in risk_keywords:
                if keyword in content:
                    risk_factors.append(keyword)
        
        return list(set(risk_factors))  # Remove duplicates
    
    def predict_market_impact(self, news_data: List[Dict[str, Any]], sectors: List[str]) -> Dict[str, Any]:
        """Predict market impact of geopolitical events"""
        try:
            # Analyze overall sentiment
            sentiment_analysis = self.analyze_news_sentiment(news_data)
            overall_sentiment = sentiment_analysis.get('average_sentiment', 0)
            
            # Predict impact for each sector
            sector_impacts = {}
            for sector in sectors:
                # Different sectors have different sensitivities to geopolitical events
                sensitivity_factors = {
                    'Technology': 0.8,  # High sensitivity
                    'Energy': 1.0,      # Very high sensitivity
                    'Finance': 0.9,     # High sensitivity
                    'Healthcare': 0.5,  # Medium sensitivity
                    'Manufacturing': 0.7, # Medium-high sensitivity
                    'Consumer Goods': 0.6 # Medium sensitivity
                }
                
                sensitivity = sensitivity_factors.get(sector, 0.7)
                impact_score = overall_sentiment * sensitivity
                
                sector_impacts[sector] = {
                    'impact_score': impact_score,
                    'volatility_prediction': abs(impact_score) * 0.5,
                    'direction': 'positive' if impact_score > 0 else 'negative',
                    'confidence': min(0.9, len(news_data) / 20)
                }
            
            return {
                'overall_sentiment': overall_sentiment,
                'sector_impacts': sector_impacts,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error predicting market impact: {e}")
            return {}
    
    def generate_investment_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate investment recommendations based on analysis"""
        recommendations = []
        
        # Basic recommendations based on sentiment
        sentiment = analysis_results.get('overall_sentiment', 0)
        
        if sentiment > 0.2:
            recommendations.extend([
                "Consider increasing exposure to growth-oriented sectors",
                "Monitor for positive geopolitical developments",
                "Look for opportunities in emerging markets"
            ])
        elif sentiment < -0.2:
            recommendations.extend([
                "Consider defensive positioning in stable sectors",
                "Increase allocation to safe-haven assets",
                "Monitor geopolitical developments closely"
            ])
        else:
            recommendations.extend([
                "Maintain balanced portfolio allocation",
                "Stay informed about geopolitical developments",
                "Consider dollar-cost averaging strategies"
            ])
        
        # Sector-specific recommendations
        sector_impacts = analysis_results.get('sector_impacts', {})
        for sector, impact in sector_impacts.items():
            if impact.get('impact_score', 0) > 0.3:
                recommendations.append(f"Consider overweighting {sector} sector")
            elif impact.get('impact_score', 0) < -0.3:
                recommendations.append(f"Consider underweighting {sector} sector")
        
        return recommendations
