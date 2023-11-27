import React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import { BarChart } from '@mui/x-charts/BarChart';

interface DataPoint {
    datetime: Date;
    engagement_rate_score: number;
  }

interface LineDatasetProps {
  data: DataPoint[];
}

const MetricChart: React.FC<LineDatasetProps> = ({ data }) => {
    // Assuming posts[index].engagement_rate contains the array of objects
    const engagementData = data;

    // Extracting datetime and engagement_rate_score arrays
    const datetimeArray = engagementData.map(entry => {
        const date = new Date(entry.datetime);
        const formattedDate = date.toLocaleDateString('en-GB'); // Use 'en-GB' locale for dd/mm/yyyy format
        return formattedDate;
      });
    const engagementRateArray = engagementData.map(entry => entry.engagement_rate_score);
    console.log("Engagement Rate Array:", engagementRateArray);
    console.log("Formatted Date Array:", datetimeArray);

  return (
   // Your BarChart component with modified props
<LineChart
  xAxis={[
    {
      id: 'datetime',
      data: datetimeArray, // Use datetime values for x-axis categories
      scaleType: 'band',
    },
  ]}
  series={[
    {
      data: engagementRateArray, // Use engagement_rate_score values for bar heights
    },
  ]}
  yAxis={[
    {
        min:0,
    }
  ]}
  width={500}
  height={300}
/>
  );
};

export default MetricChart;
