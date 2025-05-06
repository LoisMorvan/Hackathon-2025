import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface ApexChartProps {
  commune: any; // Données de la commune sélectionnée
  ecoles: any[]; // Données des écoles pour la commune
}

const ApexChart: React.FC<ApexChartProps> = ({ commune, ecoles }) => {
  const categories = ["Commerce", "Transport", "Écoles"];
  const [communeData, setCommuneData] = useState<number[]>([0, 0, 0]);
  const [ideal, setIdeal] = useState<number[]>([8, 3, 4]); // Valeurs idéales dynamiques

  useEffect(() => {
    if (commune && ecoles) {
      // Calcule le total des écoles pour la commune
      const totalEcoles = ecoles.reduce((sum, ecole) => sum + ecole.nombre_total, 0);

      // Calcule le nombre de médecins idéal pour la commune
      const idealMedecins = Math.ceil(commune.population / 1000); // 1 médecin pour 1000 habitants

      // Met à jour les données pour la commune
      setCommuneData([3, 0, totalEcoles, commune.nombre_medecins]);

      // Met à jour les valeurs idéales
      setIdeal([8, 3, 4, idealMedecins]);
    }
  }, [commune, ecoles]);

  const chartData = {
    series: [
      { name: commune.nom_commune, data: communeData },
      { name: "Idéal", data: ideal },
    ],
    options: {
      chart: {
        type: "bar", // Type de graphique
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "55%",
          borderRadius: 5,
        },
      },
      xaxis: {
        categories: categories,
      },
      yaxis: {
        title: {
          text: "Nb de services",
        },
      },
    } as ApexOptions, // Ajout explicite du type ApexOptions
  };

  return (
    <div style={{ display: "flex", justifyContent: "center" }}>
      <div style={{ width: "600px" }}>
        <ReactApexChart
          options={chartData.options}
          series={chartData.series}
          type="bar"
          height={350}
        />
      </div>
    </div>
  );
};

export default ApexChart;