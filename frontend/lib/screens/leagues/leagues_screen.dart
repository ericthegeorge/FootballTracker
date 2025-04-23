import 'package:flutter/material.dart';
import 'league_service.dart';
import '../../services/auth_service.dart';

enum LeagueScreenMode { view, select }

class LeaguesScreen extends StatefulWidget {
  final LeagueScreenMode mode;

  const LeaguesScreen({Key? key, this.mode = LeagueScreenMode.view})
    : super(key: key);

  @override
  State<LeaguesScreen> createState() => _LeaguesScreenState();
}

class _LeaguesScreenState extends State<LeaguesScreen> {
  List<String> allLeagues = [];
  List<String> filteredLeagues = [];
  Set<String> selectedLeagues = {};
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadLeagues();
  }

  Future<void> _loadLeagues() async {
    try {
      bool isAdmin = await AuthService.isAdmin();
      print('Admin status: $isAdmin');
      final leagues = await LeagueService.fetchLeagues();
      setState(() {
        allLeagues = leagues;
        filteredLeagues = List.from(leagues);
      });
    } catch (e) {
      // You could show a snackbar or error message here
      print('Failed to load leagues: $e');
    }
  }

  void _onSearchChanged(String query) {
    setState(() {
      filteredLeagues =
          allLeagues
              .where(
                (league) => league.toLowerCase().contains(query.toLowerCase()),
              )
              .toList();
    });
  }

  void _addLeague(String newLeague) async {
    final success = await LeagueService.addLeague(newLeague);
    if (success) {
      setState(() {
        allLeagues.add(newLeague);
        filteredLeagues.add(newLeague);
      });
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to add league')));
    }
  }

  void _toggleSelection(String league) {
    setState(() {
      if (selectedLeagues.contains(league)) {
        selectedLeagues.remove(league);
      } else {
        selectedLeagues.add(league);
      }
    });
  }

  void _showAddLeagueDialog() {
    String newLeague = '';
    showDialog(
      context: context,
      builder:
          (_) => AlertDialog(
            title: Text('Add League'),
            content: TextField(
              onChanged: (value) => newLeague = value,
              decoration: InputDecoration(hintText: 'Enter league name'),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  if (newLeague.trim().isNotEmpty) {
                    _addLeague(newLeague.trim());
                  }
                },
                child: Text('Add'),
              ),
            ],
          ),
    );
  }

  Widget _buildLeagueItem(String league) {
    bool isSelectable = widget.mode == LeagueScreenMode.select;
    bool isSelected = selectedLeagues.contains(league);

    return ListTile(
      title: Text(league),
      trailing:
          isSelectable
              ? Checkbox(
                value: isSelected,
                onChanged: (_) => _toggleSelection(league),
              )
              : null,
      onTap: isSelectable ? () => _toggleSelection(league) : null,
    );
  }

  @override
  Widget build(BuildContext context) {
    bool isSelectable = widget.mode == LeagueScreenMode.select;

    return Scaffold(
      appBar: AppBar(
        title: Text('Leagues'),
        actions: [
          if (isSelectable && selectedLeagues.isNotEmpty)
            TextButton(
              onPressed: () {
                // Do something with selectedLeagues
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Selected: ${selectedLeagues.join(', ')}'),
                  ),
                );
              },
              child: Text('Confirm', style: TextStyle(color: Colors.white)),
            ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: 'Search leagues...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredLeagues.length,
              itemBuilder:
                  (_, index) => _buildLeagueItem(filteredLeagues[index]),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddLeagueDialog,
        child: Icon(Icons.add),
        tooltip: 'Add League',
      ),
    );
  }
}
