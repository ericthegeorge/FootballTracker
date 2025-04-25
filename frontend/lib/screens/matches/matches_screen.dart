import 'package:flutter/material.dart';
import 'matches_service.dart';

class MatchesScreen extends StatefulWidget {
  const MatchesScreen({Key? key}) : super(key: key);

  @override
  State<MatchesScreen> createState() => _MatchesScreenState();
}

class _MatchesScreenState extends State<MatchesScreen> {
  List<MatchModel> allMatches = [];
  List<MatchModel> filteredMatches = [];
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadMatches();
  }

  Future<void> _loadMatches() async {
    try {
      final matches = await MatchesService.fetchMatches();
      setState(() {
        allMatches = matches.map((map) => MatchModel.fromMap(map)).toList();
        filteredMatches = allMatches;
      });
    } catch (e) {
      print('Failed to load matches: $e');
    }
  }

  void _onSearchChanged(String query) {
    setState(() {
      filteredMatches = allMatches.where((match) {
        return match.location.toLowerCase().contains(query.toLowerCase()) ||
               match.refereeName.toLowerCase().contains(query.toLowerCase());
      }).toList();
    });
  }

void _addMatch(MatchModel newMatch) async {
  final success = await MatchesService.addMatch(newMatch.toMap());
  if (success) {
    await _loadMatches(); // Reload from backend to avoid duplicates and get correct IDs
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Failed to add match')),
    );
  }
}

void _deleteMatch(MatchModel match) async {
  final success = await MatchesService.deleteMatch(match.matchId);
  if (success) {
    await _loadMatches(); // Reload from backend
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Match deleted')),
    );
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Failed to delete match')),
    );
  }
}

  void _showEditMatchDialog(MatchModel match) {
    TextEditingController dateController = TextEditingController(text: match.date);
    TextEditingController locationController = TextEditingController(text: match.location);
    TextEditingController startTimeController = TextEditingController(text: match.startTime);
    TextEditingController refereeNameController = TextEditingController(text: match.refereeName);
    TextEditingController endTimeController = TextEditingController(text: match.endTime);

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Edit Match'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: dateController, decoration: InputDecoration(hintText: 'Date (YYYY-MM-DD)')),
              TextField(controller: locationController, decoration: InputDecoration(hintText: 'Location')),
              TextField(controller: startTimeController, decoration: InputDecoration(hintText: 'Start Time (HH:MM:SS)')),
              TextField(controller: refereeNameController, decoration: InputDecoration(hintText: 'Referee Name')),
              TextField(controller: endTimeController, decoration: InputDecoration(hintText: 'End Time (HH:MM:SS)')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: Text('Cancel')),
          TextButton(
            onPressed: () async {
              final updatedMatch = MatchModel(
                matchId: match.matchId,
                date: dateController.text.trim(),
                location: locationController.text.trim(),
                startTime: startTimeController.text.trim(),
                refereeName: refereeNameController.text.trim(),
                endTime: endTimeController.text.trim(),
              );
              final success = await MatchesService.updateMatch(match.matchId, updatedMatch.toMap());
              if (success) {
                await _loadMatches(); // Reload from backend
                Navigator.pop(context);
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Failed to update match')),
                );
              }
            },
            child: Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showAddMatchDialog() {
    TextEditingController dateController = TextEditingController();
    TextEditingController locationController = TextEditingController();
    TextEditingController startTimeController = TextEditingController();
    TextEditingController refereeNameController = TextEditingController();
    TextEditingController endTimeController = TextEditingController();

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Add Match'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: dateController, decoration: InputDecoration(hintText: 'Date (YYYY-MM-DD)')),
              TextField(controller: locationController, decoration: InputDecoration(hintText: 'Location')),
              TextField(controller: startTimeController, decoration: InputDecoration(hintText: 'Start Time (HH:MM:SS)')),
              TextField(controller: refereeNameController, decoration: InputDecoration(hintText: 'Referee Name')),
              TextField(controller: endTimeController, decoration: InputDecoration(hintText: 'End Time (HH:MM:SS)')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: Text('Cancel')),
          TextButton(
            onPressed: () {
              if (dateController.text.trim().isNotEmpty &&
                  locationController.text.trim().isNotEmpty &&
                  startTimeController.text.trim().isNotEmpty &&
                  refereeNameController.text.trim().isNotEmpty &&
                  endTimeController.text.trim().isNotEmpty) {
                MatchModel newMatch = MatchModel(
                  matchId: 0,
                  date: dateController.text.trim(),
                  location: locationController.text.trim(),
                  startTime: startTimeController.text.trim(),
                  refereeName: refereeNameController.text.trim(),
                  endTime: endTimeController.text.trim(),
                );
                _addMatch(newMatch);
                Navigator.pop(context);
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('All fields must be filled.')),
                );
              }
            },
            child: Text('Add'),
          ),
        ],
      ),
    );
  }

  Widget _buildMatchItem(MatchModel match) {
    return ListTile(
      title: Text('${match.location} (${match.date})'),
      subtitle: Text(
          'Referee: ${match.refereeName}\n${match.startTime} - ${match.endTime}'),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          IconButton(icon: Icon(Icons.edit), onPressed: () => _showEditMatchDialog(match)),
          IconButton(icon: Icon(Icons.delete), onPressed: () => _deleteMatch(match)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Matches')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: 'Search matches...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredMatches.length,
              itemBuilder: (_, index) => _buildMatchItem(filteredMatches[index]),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddMatchDialog,
        child: Icon(Icons.add),
        tooltip: 'Add Match',
      ),
    );
  }
}

class MatchModel {
  final int matchId;
  final String date;
  final String location;
  final String startTime;
  final String refereeName;
  final String endTime;

  MatchModel({
    required this.matchId,
    required this.date,
    required this.location,
    required this.startTime,
    required this.refereeName,
    required this.endTime,
  });

  factory MatchModel.fromMap(Map<String, dynamic> map) {
    return MatchModel(
      matchId: map['match_id'],
      date: map['date'],
      location: map['location'],
      startTime: map['start_time'],
      refereeName: map['referee_name'],
      endTime: map['end_time'],
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'match_id': matchId,
      'date': date,
      'location': location,
      'start_time': startTime,
      'referee_name': refereeName,
      'end_time': endTime,
    };
  }
}
