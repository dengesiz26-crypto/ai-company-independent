import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function GmailScreen() {
  const [status, setStatus] = useState<any>({ status: 'idle' });

  useEffect(() => {
    apiGet('/api/gmail/status').then(setStatus).catch(() => setStatus({ status: 'error' }));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Gmail</Text>
      <View style={styles.card}>
        <Text style={styles.text}>Status: {status.status}</Text>
        <Text style={styles.text}>{status.email ? `Connected to ${status.email}` : 'Connect Google account to enable live mail access.'}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 28, color: theme.colors.text, marginBottom: 16 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16 },
  text: { color: theme.colors.text, fontSize: 15 },
});
