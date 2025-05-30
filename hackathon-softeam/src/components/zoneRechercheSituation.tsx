import React, { useState, useRef, useEffect } from 'react';
import { getCommunes, getCommuneInfo, getEtablissements, getEcolesStats } from "../services/services";
import ApexChart from './column-chart-situation'; // Import du composant du graphe
import '../styles/zoneRecherche.css';
import { Cartehabitant } from '../components/CarteStatistique';
import { CarteMedecin } from '../components/CarteMedecin';
import { CarteEtablissement } from '../components/CarteEtablissement';

type Commune = { nom: string };

const ZoneRecherche = () => {
  const [communes, setCommunes] = useState<Commune[]>([]);
  const searchRef = useRef<HTMLDivElement>(null);

  // Zone 1
  const [inputValue1, setInputValue1] = useState('');
  const [suggestions1, setSuggestions1] = useState<Commune[]>([]);
  const [selectedList1, setSelectedList1] = useState<Commune[]>([]);

  // Zone 2
  const [inputValue2, setInputValue2] = useState('');
  const [suggestions2, setSuggestions2] = useState<Commune[]>([]);
  const [selectedList2, setSelectedList2] = useState<Commune[]>([]);

  // État pour stocker les données du graphe
  const [chartData, setChartData] = useState<{
    communeInfo1: any[];
    communeInfo2: any[];
    etablissements1: any[];
    etablissements2: any[];
    ecoles1: any[];
    ecoles2: any[];
  } | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    getCommunes()
      .then((data) => setCommunes(data))
      .catch((error) => console.error('Erreur lors de la récupération des communes:', error));
  }, []);

  const handleChange = (
    zone: 1 | 2,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = e.target.value;
    const filtered = communes.filter(c =>
      c.nom.toLowerCase().includes(value.toLowerCase())
    );

    if (zone === 1) {
      setInputValue1(value);
      setSuggestions1(filtered);
    } else {
      setInputValue2(value);
      setSuggestions2(filtered);
    }
  };

  const handleSelect = (zone: 1 | 2, commune: Commune) => {
    const selectedList = zone === 1 ? selectedList1 : selectedList2;
    const setSelectedList = zone === 1 ? setSelectedList1 : setSelectedList2;

    const alreadySelected = selectedList.find(c => c.nom === commune.nom);
    if (alreadySelected) {
      setSelectedList(selectedList.filter(c => c.nom !== commune.nom));
    } else {
      setSelectedList([...selectedList, commune]);
    }
  };

  const handleRemove = (zone: 1 | 2, commune: Commune) => {
    const setSelectedList = zone === 1 ? setSelectedList1 : setSelectedList2;
    const selectedList = zone === 1 ? selectedList1 : selectedList2;
    setSelectedList(selectedList.filter(c => c.nom !== commune.nom));
  };

  const handleRecherche = async () => {
    try {
      setIsLoading(true);  

      const noms1 = selectedList1.map(c => c.nom);
      const noms2 = selectedList2.map(c => c.nom);
  
      // Récupération des informations des communes
      const communeInfo1 = await Promise.all(noms1.map(nom => getCommuneInfo(nom)));
      const communeInfo2 = await Promise.all(noms2.map(nom => getCommuneInfo(nom)));
  
      // Récupération des établissements pour chaque commune
      const etablissements1 = await Promise.all(
        noms1.map(nom => getEtablissements(nom))
      );
      const etablissements2 = await Promise.all(
        noms2.map(nom => getEtablissements(nom))
      );
  
      // Récupération des statistiques des écoles pour chaque commune
      const ecoles1 = await Promise.all(
        noms1.map(nom => getEcolesStats(nom))
      );
      const ecoles2 = await Promise.all(
        noms2.map(nom => getEcolesStats(nom))
      );
  
      console.log("Informations des communes pour Zone 1 :", communeInfo1);
      console.log("Établissements pour Zone 1 :", etablissements1);
      console.log("Écoles pour Zone 1 :", ecoles1);
  
      console.log("Informations des communes pour Zone 2 :", communeInfo2);
      console.log("Établissements pour Zone 2 :", etablissements2);
      console.log("Écoles pour Zone 2 :", ecoles2);
  
      // Mise à jour des données du graphe
      setChartData({
        communeInfo1,
        communeInfo2,
        etablissements1,
        etablissements2,
        ecoles1,
        ecoles2,
      });
    } catch (error) {
      console.error("Erreur lors de la recherche :", error);
      alert("Une erreur est survenue lors de la recherche.");
    } finally {
      setIsLoading(false); 
    }
  };

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setSuggestions1([]);
        setSuggestions2([]);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const renderZone = (
    zone: 1 | 2,
    inputValue: string,
    suggestions: Commune[],
    selectedList: Commune[]
  ) => (
    <div className="zone-recherche-form">
      <div className="selected-tags">
        {selectedList.map((c) => (
          <span key={c.nom} className="selected-tag">
            {c.nom}
            <button onClick={() => handleRemove(zone, c)}>×</button>
          </span>
        ))}
      </div>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => handleChange(zone, e)}
        placeholder="Entrez une commune"
        className="input-recherche"
      />
      {suggestions.length > 0 && (
        <ul className="suggestions">
          {suggestions.map((c) => (
            <li
              key={c.nom}
              className={`suggestion-item ${selectedList.find(sel => sel.nom === c.nom) ? 'selected' : ''}`}
              onClick={() => handleSelect(zone, c)}
            >
              {c.nom}
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  return (
    <div className="zone-recherche" ref={searchRef}>
      <h3>Zone de recherche</h3>
      {renderZone(1, inputValue1, suggestions1, selectedList1)}

      <button onClick={handleRecherche} className="btn-recherche">Rechercher</button>
      {isLoading && <p>Chargement des données en cours...</p>}

      {/* Affichage du graphe si les données sont disponibles */}
      {chartData && (
        <div style={{ marginTop: '50px' }}>
            <ApexChart
            commune={chartData.communeInfo1}
            ecoles={chartData.ecoles1}
            />

            {/* Calcul des totaux pour la Zone 1 */}
            <h3>Zone 1 : {chartData.communeInfo1.map(c => c.nom_commune).join(", ")}</h3>
            <Cartehabitant
            title="Habitants"
            value={chartData.communeInfo1.reduce((sum, c) => sum + (c.population || 0), 0).toLocaleString()}
            />
            <CarteMedecin
            region="Médecins / 1000 habitants"
            medecinsParHabitant={chartData.communeInfo1.reduce((sum, c) => sum + (c.ratio || 0), 0)}
            />
            <CarteEtablissement
            region="Établissements de santé"
            nombreEtablissements={chartData.etablissements1.reduce((sum, e) => sum + (e.etablissements?.length || 0), 0)}
            />

            {/* Calcul des totaux pour la Zone 2
            <h3>Zone 2 : {chartData.communeInfo2.map(c => c.nom_commune).join(", ")}</h3>
            <Cartehabitant
            title="Habitants"
            value={chartData.communeInfo2.reduce((sum, c) => sum + (c.population || 0), 0).toLocaleString()}
            />
            <CarteMedecin
            region="Médecins / 1000 habitants"
            medecinsParHabitant={chartData.communeInfo2.reduce((sum, c) => sum + (c.ratio || 0), 0)}
            />
            <CarteEtablissement
            region="Établissements de santé"
            nombreEtablissements={chartData.etablissements2.reduce((sum, e) => sum + (e.etablissements?.length || 0), 0)}
            /> */}
        </div>
        )}
    </div>
  );
};

export default ZoneRecherche;