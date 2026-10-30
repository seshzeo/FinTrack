import { useCallback, useEffect, useState } from "react";
import { api } from "../api.js";

export default function useStatistics(onError) {
  const [statistics, setStatistics] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);

  const loadStatistics = useCallback(async () => {
    setLoadingStats(true);
    try {
      setStatistics(await api.getStatistics());
    } catch (error) {
      onError(error.message);
    } finally {
      setLoadingStats(false);
    }
  }, [onError]);

  useEffect(() => {
    void loadStatistics();
  }, [loadStatistics]);

  return { statistics, loadingStats, loadStatistics };
}