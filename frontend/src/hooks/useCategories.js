import { useCallback, useEffect, useState } from "react";
import { api } from "../api.js";

export default function useCategories({ onError, onMessage, loadStatistics, onDataChanged }) {
  const [categories, setCategories] = useState([]);
  const [saving, setSaving] = useState(false);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [categoryName, setCategoryName] = useState("");

  const loadCategories = useCallback(async () => {
    try {
      setCategories(await api.getCategories());
    } catch (error) {
      onError(error.message);
    }
  }, [onError]);

  useEffect(() => {
    void loadCategories();
  }, [loadCategories]);

  function startCategory(category = null) {
    setEditingCategory(category);
    setCategoryName(category ? category.name : "");
    setCategoryOpen(true);
    onError("");
    onMessage("");
  }

  async function submitCategory(event) {
    event.preventDefault();
    setSaving(true);
    onError("");
    try {
      if (editingCategory) {
        await api.updateCategory(editingCategory.id, { name: categoryName.trim() });
        onMessage("Категория переименована.");
      } else {
        await api.createCategory({ name: categoryName.trim() });
        onMessage("Категория создана.");
      }
      setCategoryOpen(false);
      await Promise.all([loadCategories(), loadStatistics()]);
      onDataChanged();
    } catch (error) {
      onError(error.message);
    } finally {
      setSaving(false);
    }
  }

  async function removeCategory(category) {
    if (category.is_default) return;
    if (!window.confirm("Удалить категорию «" + category.name + "»?")) return;
    onError("");
    try {
      await api.deleteCategory(category.id);
      onMessage("Категория удалена.");
      await Promise.all([loadCategories(), loadStatistics()]);
      onDataChanged();
    } catch (error) {
      onError(error.message);
    }
  }

  return {
    categories,
    saving,
    categoryOpen,
    setCategoryOpen,
    editingCategory,
    categoryName,
    setCategoryName,
    startCategory,
    submitCategory,
    removeCategory,
  };
}