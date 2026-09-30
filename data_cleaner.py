import pandas as pd
import numpy as np
import re

class DataCleaner:
    """
    Módulo utilitário para higienização e padronização de DataFrames em
    projetos de análise financeira e imobiliária.
    """

    @staticmethod
    def clean_currency(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Converte colunas monetárias em texto (ex: 'R$ 1.250,50' ou '$1,250.50')
        para valores numéricos float.
        """
        df_cleaned = df.copy()
        for col in columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = (
                    df_cleaned[col]
                    .astype(str)
                    .str.replace(r'[R$\s]', '', regex=True)
                    .str.replace('.', '', regex=False)
                    .str.replace(',', '.', regex=False)
                )
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        return df_cleaned

    @staticmethod
    def standardize_dates(df: pd.DataFrame, columns: list, date_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        Padroniza colunas de data para o formato datetime e aplica a formatação desejada.
        """
        df_cleaned = df.copy()
        for col in columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce').dt.strftime(date_format)
        return df_cleaned

    @staticmethod
    def clean_text_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Remove espaços em branco nas extremidades, converte para minúsculas
        e elimina caracteres especiais desnecessários de textos/endereços.
        """
        df_cleaned = df.copy()
        for col in columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = (
                    df_cleaned[col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .str.replace(r'\s+', ' ', regex=True)
                )
        return df_cleaned

    @staticmethod
    def handle_missing_data(df: pd.DataFrame, strategy: dict) -> pd.DataFrame:
        """
        Aplica estratégias customizadas para preenchimento de valores nulos por coluna.
        Exemplo de estratégia: {'valor': 0, 'bairro': 'desconhecido'}
        """
        df_cleaned = df.copy()
        return df_cleaned.fillna(value=strategy)

    @staticmethod
    def remove_outliers_iqr(df: pd.DataFrame, column: str, factor: float = 1.5) -> pd.DataFrame:
        """
        Remove registos discrepantes (outliers) com base no intervalo interquartil (IQR).
        """
        if column not in df.columns:
            return df

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (factor * iqr)
        upper_bound = q3 + (factor * iqr)

        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
