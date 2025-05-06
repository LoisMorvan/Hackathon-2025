import React from 'react';



type CarteVilleProps = {
  ville: string;
};

export const CarteVille: React.FC<CarteVilleProps> = ({ ville}) => {
  return (
    <div className="ville-card">
      <div className="ville-title">{ville.toUpperCase()}</div>
    </div>
  );
};
