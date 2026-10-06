import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function DashboardScreen() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    apiGet('/api/dashboard').then(setData).catch(() => setData({ error: 'Backend not reachable' }));
  }, []);

  if (!data) {
    return <Text style={styles.loading}>Loading dashboard...</Text>;
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>AICorpOS</Text>
      <Text style={styles.subtitle}>AI company operating system</Text>

      {data.error ? (
        <View style={styles.card}><Text style={styles.cardText}>{data.error}</Text></View>
      ) : (
        <>
          <View style={styles.grid}>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Agents</Text><Text style={styles.kpiValue}>{data.stats?.agents ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Tasks</Text><Text style={styles.kpiValue}>{data.stats?.tasks_total ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Completed</Text><Text style={styles.kpiValue}>{data.stats?.tasks_completed ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Queued</Text><Text style={styles.kpiValue}>{data.stats?.tasks_queued ?? 0}</Text></View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Company</Text>
            <Text style={styles.cardText}>{data.company?.name} — {data.company?.objective}</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Top agents</Text>
            {data.agents?.slice(0, 5).map((agent: any) => (
              <Text key={agent.id} style={styles.cardText}>{agent.name} • {agent.role}</Text>
            ))}
          </View>
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20, paddingBottom: 60 },
  title: { color: theme.colors.text, fontSize: 32, fontWeight: '700' },
  subtitle: { color: theme.colors.muted, fontSize: 16, marginBottom: 18 },
  loading: { flex: 1, backgroundColor: theme.colors.background, color: theme.colors.text, textAlign: 'center', paddingTop: 80 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 18 },
  kpi: { width: '48%', backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  kpiLabel: { color: theme.colors.muted, fontSize: 12 },
  kpiValue: { color: theme.colors.text, fontSize: 26, fontWeight: '700' },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  sectionTitle: { fontSize: 18, color: theme.colors.text, marginBottom: 8 },
  cardText: { color: theme.colors.text, fontSize: 14 },
});
