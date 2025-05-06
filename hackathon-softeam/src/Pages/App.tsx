
import '../App.css';
import Navbar from '../Navbar';
import CityTable from '../CityTable';

function App() {
  return (
    <div lang="fr">
      <Navbar /> 
      <main> 
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

