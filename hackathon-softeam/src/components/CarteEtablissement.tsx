import React from 'react';
import './CarteEtablissement.css';

type CarteEtablissementProps = {
  region: string;
  nombreEtablissements: number;
};

export const CarteEtablissement: React.FC<CarteEtablissementProps> = ({ region, nombreEtablissements }) => {
  return (
    <div className="etablissement-card">
      <div className="etablissement-region">{region.toUpperCase()}</div>
      <div className="etablissement-value">{nombreEtablissements.toLocaleString()} établissements</div>
    </div>
  );
};
