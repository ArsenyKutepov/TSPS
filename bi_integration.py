import pandas as pd
import powerbi


class PowerBIExporter:
    def __init__(self, api_key):
        self.client = powerbi.PowerBIClient(api_key)

    def export_heatmap(self, metrics):
        """Экспорт heatmap в Power BI"""
        df = pd.DataFrame({
            'Блок': list(metrics.keys()),
            'Уровень': list(metrics.values())
        })

        dataset = self.client.create_dataset("Цифровая зрелость")
        dataset.add_dataframe(df)

        # Автогенерация визуализации
        return dataset.create_visualization(
            type='heatmap',
            x_axis='Блок',
            y_axis='Уровень'
        )