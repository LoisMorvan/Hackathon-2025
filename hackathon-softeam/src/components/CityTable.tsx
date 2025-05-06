import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ZoneRecherche from './zoneRecherche';
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
  const [filteredCommunes, setFilteredCommunes] = useState<Commune[]>([]);
  const [selectedCommunes, setSelectedCommunes] = useState<Commune[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCommunes = async () => {
      try {
        const response = await axios.get<Commune[]>('http://localhost:8000/commune-info');
        setCommunes(response.data);
        setFilteredCommunes(response.data); 
        setLoading(false);
      } catch (err) {
        setError('Erreur lors de la récupération des données.');
        setLoading(false);
      }
    };

    fetchCommunes();
  }, []);

  const handleSearch = (searchTerm: string) => {
    const filtered = communes.filter((commune) =>
      commune.nom_commune.toLowerCase().includes(searchTerm.toLowerCase()) ||
      commune.code_postal.includes(searchTerm)
    );
    setFilteredCommunes(filtered);
  };

  const handleSelect = (selected: { nom: string }[]) => {
    // Trouver les communes sélectionnées dans la liste des communes existantes
    const selectedDetails = selected
      .map((selectedCommune) =>
        communes.find((commune) => commune.nom_commune === selectedCommune.nom)
      )
      .filter((commune): commune is Commune => commune !== undefined);

    // Ajouter les communes sélectionnées sans doublons
    const updatedSelectedCommunes = [...selectedCommunes];
    selectedDetails.forEach((commune) => {
      if (!updatedSelectedCommunes.some((c) => c.nom_commune === commune.nom_commune)) {
        updatedSelectedCommunes.push(commune);
      }
    });

    setSelectedCommunes(updatedSelectedCommunes);
  };



  const handleRemoveFromComparison = (communeName: string) => {
    
    const updatedSelectedCommunes = selectedCommunes.filter(
      (commune) => commune.nom_commune !== communeName
    );
    setSelectedCommunes(updatedSelectedCommunes);
    };

    if (loading) {
      return <p>Chargement des données...</p>;
    }

    if (error) {
      return <p>{error}</p>;
    }

  return (
    <div className="city-table-container">
      {/* Zone de recherche */}
      <ZoneRecherche
        onSearch={handleSearch}
        onSelect={handleSelect}
        onRemove={handleRemoveFromComparison} 
      />

      {/* Tableau des villes comparées */}
      {selectedCommunes.length > 0 && (
        <div>
          <h2>Villes comparées</h2>
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
              {selectedCommunes.map((commune, index) => {
                const ratio = commune.nombre_medecins > 0
                  ? ((commune.nombre_medecins / commune.population) * 1000).toFixed(2)
                  : 0;

                const getBackgroundColor = (ratio: string | number) => {
                  if (ratio === 'N/A') return '#f2f2f2'; // Gris clair pour les valeurs non applicables
                  const numericRatio = parseFloat(ratio as string);
                  if (numericRatio < 2) return '#ffcccc'; // Rouge clair pour les ratios faibles
                  if (numericRatio < 3.3) return '#fff5cc'; // Jaune clair pour les ratios moyens
                  return '#ccffcc'; // Vert clair pour les ratios élevés
                };

                return (
                  <tr key={index} style={{ backgroundColor: getBackgroundColor(ratio) }}>
                    <td>{commune.nom_commune}</td>
                    <td>{commune.code_postal}</td>
                    <td>{commune.population}</td>
                    <td>{commune.nombre_medecins}</td>
                    <td>{ratio}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Tableau des communes */}
      <h2>Liste complète</h2>
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
          {filteredCommunes
            .sort((a, b) => {
              const ratioA = a.nombre_medecins > 0 ? a.population / a.nombre_medecins : Infinity;
              const ratioB = b.nombre_medecins > 0 ? b.population / b.nombre_medecins : Infinity;
              return ratioB - ratioA; // Trier par ratio décroissant
            })
            .map((commune, index) => {
              const ratio = commune.nombre_medecins > 0
                ? ((commune.nombre_medecins / commune.population) * 1000).toFixed(2)
                : 0;

              const getBackgroundColor = (ratio: string | number) => {
                if (ratio === 'N/A') return '#f2f2f2'; // Gris clair pour les valeurs non applicables
                const numericRatio = parseFloat(ratio as string);
                if (numericRatio < 2) return '#ffcccc'; // Rouge clair pour les ratios faibles
                if (numericRatio < 3.3) return '#fff5cc'; // Jaune clair pour les ratios moyens
                return '#ccffcc'; // Vert clair pour les ratios élevés
              };

              return (
                <tr key={index} style={{ backgroundColor: getBackgroundColor(ratio) }}>
                  <td>{commune.nom_commune}</td>
                  <td>{commune.code_postal}</td>
                  <td>{commune.population}</td>
                  <td>{commune.nombre_medecins}</td>
                  <td>{ratio}</td>
                </tr>
              );
            })}
        </tbody>
      </table>
    </div>
  );
};

export default CityTable;