import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

interface ApexChartProps {
  ville1: any[];
  ville2: any[];
}

const ApexChart: React.FC<ApexChartProps> = ({ ville1, ville2 }) => {
  const categories = ["Commerce", "Transport", "Scolarité"];
  const [ville1Data, setVille1Data] = useState<number[]>([0, 0, 0]);
  const [ville2Data, setVille2Data] = useState<number[]>([0, 0, 0]);
  const ideal = [8, 3, 4];

  useEffect(() => {
    if (ville1) {
      // Simule les données pour Ville 1
      setVille1Data([3, 0, 2]); // Remplace par des données dynamiques si nécessaire
    }
    if (ville2) {
      // Simule les données pour Ville 2
      setVille2Data([6, 4, 1]); // Remplace par des données dynamiques si nécessaire
    }
  }, [ville1, ville2]);

  const chartData = {
    series: [
      { name: "Ville 1", data: ville1Data },
      { name: "Ville 2", data: ville2Data },
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