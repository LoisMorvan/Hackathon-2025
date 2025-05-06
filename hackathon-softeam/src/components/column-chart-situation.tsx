import React, { useState } from "react";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";

type SeriesType = ApexAxisChartSeries;

const ApexChart: React.FC = () => {
  
  const categories = ["Commerce", "Transport", "Scolarité"];
  const ville1 = [3, 0, 2];
  const ideal = [8, 3, 4];

  const [chartData] = useState<{
    series: SeriesType;
    options: ApexOptions;
  }>( {
    series: [
      { name: "Ville 1", data: ville1 },
      { name: "Idéal", data: ideal },
    ],
    options: {
      chart: {
        type: "bar",
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "55%",
          borderRadius: 5,
          borderRadiusApplication: "end",
          distributed: false,
        },
      },
      dataLabels: {
        enabled: true,
        formatter: function (val: number, opts: any) {
          const seriesIndex = opts.seriesIndex;
          const dataPointIndex = opts.dataPointIndex;
          const idealVal = ideal[dataPointIndex];
        
          if (seriesIndex === 0) {
            return val > idealVal ? "✓" : "✗";
          }
        
          return "";
        },
        style: {
          fontSize: "18px",
          colors: ["#000"],
        },
        offsetY: -10,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ["transparent"],
      },
      xaxis: {
        categories: categories,
      },
      yaxis: {
        title: {
          text: "Nb de services",
        },
      },
      fill: {
        opacity: 1,
        colors: [
          function ({ seriesIndex }: { seriesIndex: number; dataPointIndex: number }) {
            if (seriesIndex === 0) return "#FFA500"; // orange pour "Idéal"
            if (seriesIndex === 1) return "#3A9D23"; // vert pour "Idéal"
          },
        ] as NonNullable<ApexOptions["fill"]>["colors"],
      },
      tooltip: {
        y: {
          formatter: (
            val: number,
            { dataPointIndex }: { seriesIndex: number; dataPointIndex: number }
          ): string => {
            const category = categories[dataPointIndex];
            return `${val} ${category}`;
          },
        },
      },
    },
  });

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
