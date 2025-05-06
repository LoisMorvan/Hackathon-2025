import React, { useEffect, useState } from 'react';
import { getCouvertures } from '../services/services';
import './CouvertureCards.css';

interface CouvertureData {
  bonne: string;
  moyenne: string;
  "sous-dote": string;
}

const CouvertureCards: React.FC = () => {
  const [couvertures, setCouvertures] = useState<CouvertureData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCouvertures = async () => {
      try {
        const data = await getCouvertures();
        setCouvertures(data);
      } catch (err) {
        console.error('Erreur lors de la récupération des couvertures:', err);
        setError('Impossible de récupérer les données.');
      } finally {
        setLoading(false);
      }
    };

    fetchCouvertures();
  }, []);

  if (loading) {
    return <div>Chargement des données...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div>
      <h1>Pourcentages de couverture médicale des communes de la Loire-Atlantique</h1>
      <div className="couverture-cards">
        <div className="couverture-card bonne">
          <h3>Bonne Couverture</h3>
          <p>{couvertures?.bonne}</p>
        </div>
        <div className="couverture-card moyenne">
          <h3>Couverture Moyenne</h3>
          <p>{couvertures?.moyenne}</p>
        </div>
        <div className="couverture-card sous-dote">
          <h3>Sous-dotée</h3>
          <p>{couvertures?.["sous-dote"]}</p>
        </div>
      </div>
    </div>
  );
};

export default CouvertureCards;