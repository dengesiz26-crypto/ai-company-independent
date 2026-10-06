import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function ResearchScreen() {
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    apiGet('/api/research').then(setResults).catch(() => setResults([]));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Market research</Text>
      {results.length === 0 ? (
        <View style={styles.card}><Text style={styles.text}>No research results yet. Trigger a research task from the manager.</Text></View>
      ) : (
        results.map((item, index) => (
          <View key={index} style={styles.card}>
            <Text style={styles.linkTitle}>{item.title}</Text>
            <Text style={styles.text}>{item.snippet}</Text>
          </View>
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 30, color: theme.colors.text, marginBottom: 18 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  linkTitle: { color: theme.colors.text, fontSize: 18, fontWeight: '700', marginBottom: 8 },
  text: { color: theme.colors.text },
});


path="frontend/app/(tabs)/research.tsx" 
