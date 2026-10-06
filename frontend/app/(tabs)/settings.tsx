import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function ResearchScreen() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    apiGet('/api/research').then(setItems).catch(() => setItems([]));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Research</Text>
      {items.map((item, index) => (
        <View key={index} style={styles.card}>
          <Text style={styles.titleSmall}>{item.title || 'Research result'}</Text>
          <Text style={styles.text}>{item.snippet || item.url || 'No summary.'}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 28, color: theme.colors.text, marginBottom: 16 },
  titleSmall: { color: theme.colors.text, fontSize: 18, fontWeight: '700', marginBottom: 6 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  text: { color: theme.colors.text },
});
