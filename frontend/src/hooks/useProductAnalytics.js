import { useEffect, useState } from 'react';
import axios from 'axios';

const EMPTY_ANALYTICS = {
  filteredData: [],
  overallStats: { current: null, min: null, max: null, avg: null },
  storeStats: []
};


export function useProductAnalytics({ selectedProductData, timeRange, storeFilter }) {
  const [analyticsData, setAnalyticsData] = useState(EMPTY_ANALYTICS);
  const [loadingAnalytics, setLoadingAnalytics] = useState(false);

  const apiUrl = import.meta.env.VITE_API_URL || '';

  async function fetchAnalytics() {
    if (!selectedProductData?.id) {
      setAnalyticsData(EMPTY_ANALYTICS);
      return;
    }

    setLoadingAnalytics(true);
    try {
      const response = await axios.get(
        `${apiUrl}/api/analytics/${selectedProductData.id}?days=${timeRange}&store=${encodeURIComponent(storeFilter || 'all')}`
      );
      setAnalyticsData(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
      setAnalyticsData(EMPTY_ANALYTICS);
    } finally {
      setLoadingAnalytics(false);
    }
  }

  useEffect(() => {
    fetchAnalytics();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedProductData?.id, timeRange, storeFilter, apiUrl]);

  const selectedProductLabel = selectedProductData
    ? selectedProductData.group_name
      ? `${selectedProductData.group_name} / ${selectedProductData.name}`
      : selectedProductData.name
    : 'Selecione um produto';

  return {
    filteredData: analyticsData.filteredData,
    overallStats: analyticsData.overallStats,
    selectedProductLabel,
    storeStats: analyticsData.storeStats,
    loadingAnalytics,
    refetchAnalytics: fetchAnalytics
  };
}
