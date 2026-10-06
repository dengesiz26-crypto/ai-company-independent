import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function CompanyScreen() {
  const [company, setCompany] = useState<any>({});

  useEffect(() => {
    apiGet('/api/company').then(setCompany).catch(() => setCompany({}));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Company</Text>
      <View style={styles.card}>
        <Text style={styles.text}>Name: {company.name || 'AICorpOS'}</Text>
        <Text style={styles.text}>Objective: {company.objective || 'Run a modern AI operations company.'}</Text>
        <Text style={styles.text}>Status: {company.status || 'running'}</Text>
        <Text style={styles.text}>Autonomy: {String(company.autonomy ?? true)}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 30, color: theme.colors.text, marginBottom: 18 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16 },
  text: { color: theme.colors.text, fontSize: 15, marginBottom: 8 },
});


path="frontend/app/(tabs)/company.tsx" 
