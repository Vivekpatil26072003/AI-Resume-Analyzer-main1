import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ScoreCardProps {
  score: number;
  className?: string;
}

const ScoreCard: React.FC<ScoreCardProps> = ({ score, className = '' }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <TrendingUp className="w-6 h-6" />;
    if (score >= 60) return <TrendingUp className="w-6 h-6" />;
    if (score >= 40) return <Minus className="w-6 h-6" />;
    return <TrendingDown className="w-6 h-6" />;
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Moderate';
    return 'Low';
  };

  return (
    <div className={`card ${getScoreColor(score)} ${className}`}>
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Match Score</h3>
          <p className="text-sm opacity-75">{getScoreLabel(score)} Match</p>
        </div>
        <div className="flex items-center space-x-2">
          {getScoreIcon(score)}
          <span className="text-3xl font-bold">{score}%</span>
        </div>
      </div>
      
      <div className="mt-4">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-500 ${
              score >= 80 ? 'bg-green-500' :
              score >= 60 ? 'bg-blue-500' :
              score >= 40 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${Math.min(score, 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;




