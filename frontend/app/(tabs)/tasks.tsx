import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { apiGet } from '../../src/api';
import { theme } from '../../src/theme';

export default function AgentsScreen() {
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    apiGet('/api/agents').then(setAgents).catch(() => setAgents([]));
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Agent team</Text>
      {agents.map((agent) => (
        <View key={agent.id} style={styles.card}>
          <Text style={styles.name}>{agent.name}</Text>
          <Text style={styles.role}>{agent.role} • {agent.department}</Text>
          <Text style={styles.text}>{agent.objective}</Text>
          <Text style={styles.meta}>Tools: {agent.tools.join(', ')}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: 20 },
  title: { fontSize: 30, color: theme.colors.text, marginBottom: 18 },
  card: { backgroundColor: theme.colors.panel, borderRadius: 14, padding: 16, marginBottom: 12 },
  name: { color: theme.colors.text, fontSize: 20, fontWeight: '700' },
  role: { color: theme.colors.primary, marginBottom: 8 },
  text: { color: theme.colors.text, marginBottom: 8 },
  meta: { color: theme.colors.muted },
});


path="frontend/app/(tabs)/agents.tsx" 
