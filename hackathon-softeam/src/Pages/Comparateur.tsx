import React from 'react';
import Navbar from '../components/Navbar';
import ZoneRecherche from '../components/zoneRechercheComparateur';

const Comparateur: React.FC = () => {
  return (
    <div>
      <Navbar />
      <main style={{ marginTop: '100px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '50px' }}>
          <div>
            <ZoneRecherche />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

const Footer = () => (
  <footer>
    <p>HACKATON - 2025 - SOFTEAM</p>
  </footer>
);

export default Comparateur;