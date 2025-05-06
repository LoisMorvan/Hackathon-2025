import React, { useState, useRef, useEffect } from 'react';
import { getCommunes } from "../services/services";
import '../styles/zoneRecherche.css';

const ZoneRecherche = () => {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<{ nom: string }[]>([]);
  const [selectedList, setSelectedList] = useState<{ nom: string }[]>([]);
  const [communes, setCommunes] = useState<{ nom: string }[]>([]);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getCommunes()
      .then((data) => {
        setCommunes(data);
      })
      .catch((error) => {
        console.error('Erreur lors de la récupération des communes:', error);
      });
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);

    const filtered = communes.filter(c =>
      c.nom.toLowerCase().includes(value.toLowerCase())
    );
    setSuggestions(filtered);
  };

  const handleSelect = (commune: { nom: string }) => {
    const alreadySelected = selectedList.find(c => c.nom === commune.nom);
    if (alreadySelected) {
      setSelectedList(selectedList.filter(c => c.nom !== commune.nom));
    } else {
      setSelectedList([...selectedList, commune]);
    }
  };

  const handleRemove = (commune: {nom: string }) => {
    setSelectedList(selectedList.filter(c => c.nom !== commune.nom));
  };

  const handleRecherche = () => {
    if (selectedList.length > 0) {
      const noms = selectedList.map(c => c.nom).join(', ');
      alert(`Recherche lancée pour : ${noms}`);
    }
  };

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setSuggestions([]);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="zone-recherche" ref={searchRef}>
      <div className="selected-tags">
        {selectedList.map((c) => (
          <span key={c.nom} className="selected-tag">
            {c.nom}
            <button onClick={() => handleRemove(c)}>×</button>
          </span>
        ))}
      </div>

      <div className="zone-recherche-form">
        <input
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Entrez une commune"
          className="input-recherche"
        />
        <button onClick={handleRecherche} className="btn-recherche">Rechercher</button>

        {suggestions.length > 0 && (
          <ul className="suggestions">
            {suggestions.map((c) => (
              <li
                key={c.nom}
                className={`suggestion-item ${selectedList.find(sel => sel.nom === c.nom) ? 'selected' : ''}`}
                onClick={() => handleSelect(c)}
              >
                {c.nom}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ZoneRecherche;
