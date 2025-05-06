import React from 'react';
import './CarteCommune.css';

type CarteCommuneProps = {
  nomCommune: string;
};

export const CarteCommune: React.FC<CarteCommuneProps> = ({ nomCommune }) => {
  return (
    <div className="commune-card">
      <div className="commune-nom">{nomCommune.toUpperCase()}</div>
    </div>
  );
};
