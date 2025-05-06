
import '../App.css';
import Navbar from '../components/Navbar';
import CityTable from '../components/CityTable';
import CouvertureCards from '../components/CouvertureCards';

function App() {
  return (
    <div lang="fr">
      <Navbar /> 
      <main> 
        <CouvertureCards />
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

