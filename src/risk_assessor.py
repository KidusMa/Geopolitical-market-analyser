import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class RiskAssessor:
    """Geopolitical risk assessment engine"""
    
    def __init__(self):
        # Risk factors and their weights
        self.risk_factors = {
            'political_stability': 0.25,
            'economic_conditions': 0.20,
            'diplomatic_relations': 0.20,
            'regional_conflicts': 0.15,
            'trade_relations': 0.10,
            'regulatory_environment': 0.10
        }
        
        # Regional risk baselines
        self.regional_baselines = {
            'North America': 0.3,
            'Europe': 0.4,
            'Asia-Pacific': 0.5,
            'Middle East': 0.7,
            'Africa': 0.6,
            'Latin America': 0.5
        }
        
        # Sector-specific risk sensitivities
        self.sector_sensitivities = {
            'Technology': {
                'political_stability': 0.8,
                'trade_relations': 0.9,
                'regulatory_environment': 0.7
            },
            'Energy': {
                'political_stability': 1.0,
                'diplomatic_relations': 0.9,
                'regional_conflicts': 0.8
            },
            'Finance': {
                'political_stability': 0.9,
                'economic_conditions': 0.8,
                'regulatory_environment': 0.9
            },
            'Healthcare': {
                'political_stability': 0.6,
                'regulatory_environment': 0.8,
                'economic_conditions': 0.7
            },
            'Manufacturing': {
                'trade_relations': 0.8,
                'economic_conditions': 0.7,
                'political_stability': 0.6
            },
            'Consumer Goods': {
                'economic_conditions': 0.8,
                'trade_relations': 0.7,
                'political_stability': 0.5
            }
        }
    
    def assess_region_risk(self, region: str) -> float:
        """Assess overall geopolitical risk for a region"""
        try:
            # Get baseline risk for the region
            baseline_risk = self.regional_baselines.get(region, 0.5)
            
            # Apply current geopolitical factors
            current_factors = self._get_current_risk_factors(region)
            
            # Calculate weighted risk score
            risk_score = baseline_risk
            for factor, weight in self.risk_factors.items():
                factor_value = current_factors.get(factor, 0.5)
                risk_score += (factor_value - 0.5) * weight
            
            # Normalize to 0-1 range
            risk_score = max(0, min(1, risk_score))
            
            return risk_score
            
        except Exception as e:
            print(f"Error assessing risk for {region}: {e}")
            return 0.5
    
    def assess_sector_risk(self, sector: str, region: str) -> Dict[str, Any]:
        """Assess risk for a specific sector in a region"""
        try:
            # Get base region risk
            region_risk = self.assess_region_risk(region)
            
            # Get sector sensitivities
            sensitivities = self.sector_sensitivities.get(sector, {})
            
            # Calculate sector-specific risk
            sector_risk = region_risk
            for factor, sensitivity in sensitivities.items():
                factor_risk = self._get_factor_risk(factor, region)
                sector_risk += (factor_risk - 0.5) * sensitivity * 0.2
            
            # Normalize to 0-1 range
            sector_risk = max(0, min(1, sector_risk))
            
            return {
                'sector': sector,
                'region': region,
                'risk_score': sector_risk,
                'risk_level': self._get_risk_level(sector_risk),
                'confidence': 0.8,
                'key_factors': self._identify_sector_risk_factors(sector, region)
            }
            
        except Exception as e:
            print(f"Error assessing sector risk: {e}")
            return {
                'sector': sector,
                'region': region,
                'risk_score': 0.5,
                'risk_level': 'Medium',
                'confidence': 0.0,
                'key_factors': ['Analysis error']
            }
    
    def get_detailed_risk_analysis(self, region: str) -> str:
        """Get detailed risk analysis for a region"""
        try:
            risk_score = self.assess_region_risk(region)
            risk_level = self._get_risk_level(risk_score)
            
            analysis = f"=== DETAILED RISK ANALYSIS: {region.upper()} ===\n\n"
            analysis += f"Overall Risk Score: {risk_score:.2f} ({risk_level})\n\n"
            
            # Factor breakdown
            analysis += "Risk Factor Breakdown:\n"
            current_factors = self._get_current_risk_factors(region)
            
            for factor, weight in self.risk_factors.items():
                factor_value = current_factors.get(factor, 0.5)
                factor_level = self._get_risk_level(factor_value)
                analysis += f"• {factor.replace('_', ' ').title()}: {factor_value:.2f} ({factor_level})\n"
            
            analysis += "\nKey Risk Indicators:\n"
            key_indicators = self._get_key_risk_indicators(region)
            for indicator in key_indicators:
                analysis += f"• {indicator}\n"
            
            analysis += "\nRecommendations:\n"
            recommendations = self._get_risk_recommendations(region, risk_score)
            for rec in recommendations:
                analysis += f"• {rec}\n"
            
            return analysis
            
        except Exception as e:
            print(f"Error generating detailed analysis for {region}: {e}")
            return f"Unable to generate detailed analysis for {region} due to an error."
    
    def _get_current_risk_factors(self, region: str) -> Dict[str, float]:
        """Get current risk factors for a region"""
        # This would integrate with real-time data sources
        # For now, return simulated data based on region
        
        base_factors = {
            'political_stability': 0.5,
            'economic_conditions': 0.5,
            'diplomatic_relations': 0.5,
            'regional_conflicts': 0.5,
            'trade_relations': 0.5,
            'regulatory_environment': 0.5
        }
        
        # Apply region-specific adjustments
        if region == 'Middle East':
            base_factors.update({
                'regional_conflicts': 0.8,
                'political_stability': 0.6,
                'diplomatic_relations': 0.7
            })
        elif region == 'Europe':
            base_factors.update({
                'political_stability': 0.7,
                'economic_conditions': 0.6,
                'regulatory_environment': 0.8
            })
        elif region == 'Asia-Pacific':
            base_factors.update({
                'trade_relations': 0.6,
                'diplomatic_relations': 0.7,
                'economic_conditions': 0.6
            })
        elif region == 'North America':
            base_factors.update({
                'political_stability': 0.8,
                'economic_conditions': 0.7,
                'regulatory_environment': 0.8
            })
        
        return base_factors
    
    def _get_factor_risk(self, factor: str, region: str) -> float:
        """Get risk level for a specific factor in a region"""
        current_factors = self._get_current_risk_factors(region)
        return current_factors.get(factor, 0.5)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score > 0.7:
            return 'High'
        elif risk_score > 0.4:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_sector_risk_factors(self, sector: str, region: str) -> List[str]:
        """Identify key risk factors for a sector in a region"""
        factors = []
        
        # Get sector sensitivities
        sensitivities = self.sector_sensitivities.get(sector, {})
        
        # Check which factors are most sensitive for this sector
        for factor, sensitivity in sensitivities.items():
            if sensitivity > 0.7:  # High sensitivity
                factor_risk = self._get_factor_risk(factor, region)
                if factor_risk > 0.6:  # High risk
                    factors.append(f"High {factor.replace('_', ' ')} risk")
        
        # Add general factors
        if sector == 'Energy':
            factors.extend(['Oil price volatility', 'Supply chain disruptions'])
        elif sector == 'Technology':
            factors.extend(['Regulatory changes', 'Trade restrictions'])
        elif sector == 'Finance':
            factors.extend(['Interest rate changes', 'Currency volatility'])
        
        return factors if factors else ['Moderate risk factors']
    
    def _get_key_risk_indicators(self, region: str) -> List[str]:
        """Get key risk indicators for a region"""
        indicators = []
        
        if region == 'Middle East':
            indicators.extend([
                'Ongoing regional conflicts',
                'Oil price volatility',
                'Diplomatic tensions',
                'Political instability'
            ])
        elif region == 'Europe':
            indicators.extend([
                'Brexit implications',
                'EU policy changes',
                'Economic sanctions',
                'Migration challenges'
            ])
        elif region == 'Asia-Pacific':
            indicators.extend([
                'US-China trade relations',
                'Territorial disputes',
                'Supply chain disruptions',
                'Currency fluctuations'
            ])
        elif region == 'North America':
            indicators.extend([
                'Policy uncertainty',
                'Trade agreements',
                'Regulatory changes',
                'Economic recovery'
            ])
        
        return indicators
    
    def _get_risk_recommendations(self, region: str, risk_score: float) -> List[str]:
        """Get risk mitigation recommendations"""
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.extend([
                'Consider reducing exposure to high-risk regions',
                'Implement strict risk management protocols',
                'Monitor geopolitical developments closely',
                'Diversify investments across multiple regions'
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                'Maintain balanced portfolio allocation',
                'Stay informed about regional developments',
                'Consider hedging strategies',
                'Monitor key risk indicators'
            ])
        else:
            recommendations.extend([
                'Consider increasing exposure to stable regions',
                'Look for growth opportunities',
                'Monitor for emerging risks',
                'Maintain standard risk management'
            ])
        
        # Region-specific recommendations
        if region == 'Middle East':
            recommendations.append('Monitor oil price movements and supply disruptions')
        elif region == 'Europe':
            recommendations.append('Track EU policy developments and regulatory changes')
        elif region == 'Asia-Pacific':
            recommendations.append('Monitor US-China relations and trade policies')
        
        return recommendations
    
    def calculate_portfolio_risk(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall portfolio risk based on geopolitical factors"""
        try:
            total_risk = 0
            weighted_risk = 0
            total_allocation = 0
            
            for position in portfolio_data:
                sector = position.get('sector', 'Unknown')
                region = position.get('region', 'Unknown')
                allocation = position.get('allocation', 0)
                
                # Get sector risk
                sector_risk = self.assess_sector_risk(sector, region)
                risk_score = sector_risk.get('risk_score', 0.5)
                
                total_risk += risk_score
                weighted_risk += risk_score * allocation
                total_allocation += allocation
            
            if total_allocation > 0:
                avg_risk = total_risk / len(portfolio_data)
                weighted_avg_risk = weighted_risk / total_allocation
            else:
                avg_risk = 0.5
                weighted_avg_risk = 0.5
            
            return {
                'average_risk': avg_risk,
                'weighted_risk': weighted_avg_risk,
                'risk_level': self._get_risk_level(weighted_avg_risk),
                'total_positions': len(portfolio_data),
                'high_risk_positions': sum(1 for p in portfolio_data 
                                         if self.assess_sector_risk(p.get('sector', ''), p.get('region', '')).get('risk_score', 0) > 0.7)
            }
            
        except Exception as e:
            print(f"Error calculating portfolio risk: {e}")
            return {
                'average_risk': 0.5,
                'weighted_risk': 0.5,
                'risk_level': 'Medium',
                'total_positions': 0,
                'high_risk_positions': 0
            }
