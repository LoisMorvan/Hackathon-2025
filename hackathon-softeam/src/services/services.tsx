import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Remplace par l'URL de ton backend si nécessaire

/**
 * Récupère la liste des communes en Loire-Atlantique.
 * @param value Nom ou code postal (facultatif).
 * @returns Liste des communes.
 */
export const getCommunes = async (value?: string) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/communes`, {
      params: { value },
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des communes:", error);
    throw error;
  }
};

/**
 * Récupère les informations enrichies d'une commune.
 * @param value Nom ou code postal de la commune (facultatif).
 * @returns Informations enrichies de la commune.
 */
export const getCommuneInfo = async (value?: string) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/commune-info`, {
      params: { value },
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des informations de la commune:", error);
    throw error;
  }
};

/**
 * Récupère les établissements pour une commune donnée.
 * @param commune Nom de la commune.
 * @param categorie Catégorie d'établissement (facultatif, par défaut "Maison de santé (L.6223-3)").
 * @returns Liste des établissements.
 */
export const getEtablissements = async (commune: string, categorie?: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/etablissements`, {
        params: { commune, categorie },
      });
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des établissements:", error);
      throw error;
    }
};

/**
 * Récupère les statistiques des écoles pour une ville donnée.
 * @param ville Nom de la ville (facultatif).
 * @returns Statistiques des écoles.
 */
export const getEcolesStats = async (ville?: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/ecoles/stats`, {
        params: { ville },
      });
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des statistiques des écoles:", error);
      throw error;
    }
  };
  
  /**
   * Récupère les pourcentages de couverture médicale des communes.
   * @returns Pourcentages de couverture médicale.
   */
  export const getCouvertures = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/couvertures`);
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des couvertures médicales:", error);
      throw error;
    }
  };