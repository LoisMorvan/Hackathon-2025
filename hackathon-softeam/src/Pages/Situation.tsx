import React from 'react';
import Navbar from '../components/Navbar';
import ZoneRecherche from '../components/zoneRechercheSituation';

const Situation: React.FC = () => {
    return (
        <div>
          <Navbar />
          <main style={{ marginTop: '100px' }}>
            <ZoneRecherche />
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
    

export default Situation;