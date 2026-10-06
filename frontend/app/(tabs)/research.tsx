import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function GmailScreen() {
  const [status, setStatus] = useState<any>({ status: 'disconnected' });

  useEffect(() => {
    apiGet('/api/gmail/status').then(setStatus).catch(() => setStatus({ status: 'error' }));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Gmail connective</Text>
      <View style={styles.card}>
        <Text style={styles.text}>Status: {status.status}</Text>
        <Text style={styles.text}>{status.email ? `Connected to ${status.email}` : 'Ready for Gmail OAuth flow'}</Text>
        <Text style={styles.text}>This app uses a simple OAuth-ready flow so users can authorize Gmail without manual client setup inside the app.</Text>
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


path="frontend/app/(tabs)/gmail.tsx" 
