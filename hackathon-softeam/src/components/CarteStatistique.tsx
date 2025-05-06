import React from 'react';
import './CarteStatistique.css';


type Cartehabitant = {
  title: string;
  value: string | number;
};

export const Cartehabitant: React.FC<Cartehabitant> = ({ title, value }) => {
  return (
    <div className="stat-card">
      <div className="stat-title">{title.toUpperCase()}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
};
