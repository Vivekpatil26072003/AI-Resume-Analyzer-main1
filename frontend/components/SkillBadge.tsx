import React from 'react';

interface SkillBadgeProps {
  skill: string;
  variant?: 'default' | 'matched' | 'missing';
  className?: string;
}

const SkillBadge: React.FC<SkillBadgeProps> = ({ 
  skill, 
  variant = 'default',
  className = ''
}) => {
  const baseClasses = 'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium';
  
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    matched: 'bg-green-100 text-green-800',
    missing: 'bg-red-100 text-red-800'
  };

  return (
    <span className={`${baseClasses} ${variantClasses[variant]} ${className}`}>
      {skill}
    </span>
  );
};

export default SkillBadge;

