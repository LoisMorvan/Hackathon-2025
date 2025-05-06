
import '../App.css';
import Navbar from '../components/Navbar';
import CityTable from '../components/CityTable';
import ZoneRecherche from '../components/zoneRecherche';

function App() {
  return (
    <div lang="fr">
      <Navbar /> 
      <main> 
        <ZoneRecherche />
        <CityTable />
      </main>
      <Footer />
    </div>
  );
}







const Footer = () => (
  <footer>
    <p>HACKATON - 2025 - SOFTEAM</p>
  </footer>
);

export default App;

