import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CityTable.css'; 

interface Commune {
  nom_commune: string;
  code_postal: string;
  population: number;
  nombre_medecins: number;
  ration: number | null;
  coordonnees: {
    lat: number;
    lon: number;
  };
}

const CityTable: React.FC = () => {
  const [communes, setCommunes] = useState<Commune[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCommunes = async () => {
      try {
        const response = await axios.get<Commune[]>('http://localhost:8000/commune-info');
        setCommunes(response.data);
        setLoading(false);
      } catch (err) {
        setError('Erreur lors de la récupération des données.');
        setLoading(false);
      }
    };

    fetchCommunes();
  }, []);

  if (loading) {
    return <p>Chargement des données...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="city-table-container">
      <h2>Liste des Communes</h2>
      <table className="city-table">
        <thead>
          <tr>
            <th>Nom de la Commune</th>
            <th>Code Postal</th>
            <th>Population</th>
            <th>Nombre de Médecins</th>
            <th>Ratio (Habitants/Médecin)</th>
          </tr>
        </thead>
        <tbody>
          {communes.map((commune, index) => (
            <tr key={index}>
              <td>{commune.nom_commune}</td>
              <td>{commune.code_postal}</td>
              <td>{commune.population}</td>
              <td>{commune.nombre_medecins}</td>
              <td>{commune.ration !== null ? commune.ration : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CityTable;
