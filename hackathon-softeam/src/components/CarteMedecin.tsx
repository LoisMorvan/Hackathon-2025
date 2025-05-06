import React from 'react';
import './CarteMedecin.css';

type CarteMedecinProps = {
  region: string;
  medecinsParHabitant: number;
};

export const CarteMedecin: React.FC<CarteMedecinProps> = ({ region, medecinsParHabitant }) => {
  return (
    <div className="medecin-card">
      <div className="medecin-region">{region.toUpperCase()}</div>
      <div className="medecin-value">{medecinsParHabitant.toFixed(2)}</div>
    </div>
  );
};
