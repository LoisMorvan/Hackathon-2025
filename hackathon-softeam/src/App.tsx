import React from 'react';
import logo from './logo.svg';
import { Cartehabitant } from './components/CarteStatistique';
import { CarteVille } from './components/CarteVille';
import { CarteMedecin } from './components/CarteMedecin';
import { CarteEtablissement } from './components/CarteEtablissement';
import { CarteCommune } from './components/CarteCommune';

function App() {
  return (
    <div className="App">
      <Cartehabitant title="Habitants " value="1,521" />
      <CarteVille ville="Nantes"/>
      <CarteMedecin region="Nantes" medecinsParHabitant={25} />
      <CarteEtablissement region="Nantes" nombreEtablissements={1345} />
      <CarteCommune nomCommune="Nom de la commune" />
    </div>
  );
}
export default App;

