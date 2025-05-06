import React, { useState, useRef, useEffect } from 'react';
import { getCommunes } from "../services/services";
import '../styles/zoneRecherche.css';

interface ZoneRechercheProps {
  onSearch?: (searchTerm: string) => void; // Transmet le terme de recherche au parent
  onSelect?: (selectedCommunes: { nom: string }[]) => void; // Transmet les villes sélectionnées au parent
}

const ZoneRecherche: React.FC<ZoneRechercheProps> = ({ onSearch, onSelect }) => {
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

    if (onSearch) {
      onSearch(value); // Transmet le terme de recherche au parent
    }
  };

  const handleSelect = (commune: { nom: string }) => {
    const alreadySelected = selectedList.find(c => c.nom === commune.nom);
    if (!alreadySelected) {
      const updatedList = [...selectedList, commune];
      setSelectedList(updatedList);

      // Transmet les villes sélectionnées au parent
      if (onSelect) {
        onSelect(updatedList);
      }
    }
    setInputValue(''); // Réinitialise le champ de recherche
    setSuggestions([]); // Cache les suggestions
  };

  const handleRemove = (commune: { nom: string }) => {
    const updatedList = selectedList.filter(c => c.nom !== commune.nom);
    setSelectedList(updatedList);

    // Transmet les villes sélectionnées au parent
    if (onSelect) {
      onSelect(updatedList);
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

        {suggestions.length > 0 && (
          <ul className="suggestions">
            {suggestions.map((c) => (
              <li
                key={c.nom}
                className="suggestion-item"
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