import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface ApexChartProps {
  ville1: any[];
  ville2: any[];
  ecoles1: any[];
  ecoles2: any[];
}

const ApexChart: React.FC<ApexChartProps> = ({ ville1, ville2, ecoles1, ecoles2 }) => {
  const categories = ["Commerce", "Transport", "Ecoles"];
  const [ville1Data, setVille1Data] = useState<number[]>([0, 0, 0]);
  const [ville2Data, setVille2Data] = useState<number[]>([0, 0, 0]);
  const ideal = [8, 3, 4];

  const ville1Name = ville1.map(v => v.nom_commune).join(", ");
  const ville2Name = ville2.map(v => v.nom_commune).join(", ");

  useEffect(() => {
    if (ville1 && ecoles1) {
      // Calcule le total des écoles pour Ville 1
      const totalEcoles1 = ecoles1.reduce((sum, ecole) => sum + ecole.nombre_total, 0);
      setVille1Data([3, 0, totalEcoles1]); // Ajoute le total des écoles comme 4e valeur
    }
    if (ville2 && ecoles2) {
      // Calcule le total des écoles pour Ville 2
      const totalEcoles2 = ecoles2.reduce((sum, ecole) => sum + ecole.nombre_total, 0);
      setVille2Data([6, 4, totalEcoles2]); // Ajoute le total des écoles comme 4e valeur
    }
  }, [ville1, ville2, ecoles1, ecoles2]);

  const chartData = {
    series: [
      { name: ville1Name, data: ville1Data },
      { name: ville2Name, data: ville2Data },
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