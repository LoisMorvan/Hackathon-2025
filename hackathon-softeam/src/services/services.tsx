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