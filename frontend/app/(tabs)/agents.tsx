import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function DashboardScreen() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const result = await apiGet('/api/dashboard');
        setData(result);
      } catch {
        setData({ error: 'Backend is not reachable. Start the FastAPI server first.' });
      }
    };
    load();
  }, []);

  if (!data) {
    return <Text style={styles.loading}>Loading company dashboard…</Text>;
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{data.company?.name || 'AICorpOS'}</Text>
      <Text style={styles.subtitle}>{data.company?.objective || 'AI company operating system'}</Text>

      {data.error ? (
        <View style={styles.card}><Text style={styles.cardText}>{data.error}</Text></View>
      ) : (
        <>
          <View style={styles.grid}>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Agents</Text><Text style={styles.kpiValue}>{data.stats?.agents ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Tasks</Text><Text style={styles.kpiValue}>{data.stats?.tasks_total ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Completed</Text><Text style={styles.kpiValue}>{data.stats?.tasks_completed ?? 0}</Text></View>
            <View style={styles.kpi}><Text style={styles.kpiLabel}>Notifications</Text><Text style={styles.kpiValue}>{data.stats?.notifications ?? 0}</Text></View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Active company</Text>
            <Text style={styles.cardText}>Status: {data.company?.status || 'running'}</Text>
            <Text style={styles.cardText}>Autonomy: {String(data.company?.autonomy ?? true)}</Text>
            <Text style={styles.cardText}>Budget: ${data.company?.budget ?? 0}</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Live agent roster</Text>
            {data.agents?.map((agent: any) => (
              <Text key={agent.id} style={styles.rowText}>{agent.name} • {agent.role}</Text>
            ))}
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Free resources</Text>
            {data.resources?.map((resource: any, idx: number) => (
              <Text key={idx} style={styles.rowText}>{resource.name}</Text>
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
  title: { color: theme.colors.text, fontSize: 30, fontWeight: '700' },
  subtitle: { color: theme.colors.muted, fontSize: 15, marginBottom: 18 },
  loading: { flex: 1, backgroundColor: theme.colors.background, color: theme.colors.text, textAlign: 'center', paddingTop: 80 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 18 },
  kpi: { width: '48%', backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  kpiLabel: { color: theme.colors.muted, fontSize: 12 },
  kpiValue: { color: theme.colors.text, fontSize: 24, fontWeight: '700' },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  sectionTitle: { color: theme.colors.text, fontSize: 18, fontWeight: '700', marginBottom: 8 },
  cardText: { color: theme.colors.text, marginBottom: 4 },
  rowText: { color: theme.colors.text, marginBottom: 5 },
});


path="frontend/app/(tabs)/dashboard.tsx" 
