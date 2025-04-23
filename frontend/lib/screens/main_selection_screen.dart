import 'package:flutter/material.dart';
import 'package:frontend/routes.dart';
import 'leagues/leagues_screen.dart';
import 'teams/teams_screen.dart';
import 'players/players_screen.dart';
import 'matches/matches_screen.dart';
import 'account_settings_screen.dart';

class MainSelectionScreen extends StatelessWidget {
  void navigateToScreen(BuildContext context, String screen) {
    switch (screen) {
      case Routes.leagues:
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => LeaguesScreen()),
        );
        break;
      case Routes.teams:
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => TeamsScreen()),
        );
        break;
      case Routes.players:
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => PlayersScreen()),
        );
        break;
      case Routes.matches:
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => MatchesScreen()),
        );
        break;
      case Routes.account_settings:
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => AccountSettingsScreen()),
        );
        break;
      default:
        print('Invalid screen');
    }
  }

  Widget buildCard({
    required BuildContext context,
    required String title,
    required IconData icon,
    required String imagePath,
    required String route,
  }) {
    return GestureDetector(
      onTap: () => navigateToScreen(context, route),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          image: DecorationImage(
            image: AssetImage(imagePath),
            fit: BoxFit.cover,
            colorFilter: ColorFilter.mode(
              Colors.black.withOpacity(0.45),
              BlendMode.darken,
            ),
          ),
        ),
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 36, color: Colors.white),
              const SizedBox(height: 8),
              Text(
                title,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Main Selection')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          children: [
            buildCard(
              context: context,
              title: 'Leagues',
              icon: Icons.emoji_events,
              imagePath: 'assets/images/leagues.jpg',
              route: Routes.leagues,
            ),
            buildCard(
              context: context,
              title: 'Teams',
              icon: Icons.groups,
              imagePath: 'assets/images/teams.jpg',
              route: Routes.teams,
            ),
            buildCard(
              context: context,
              title: 'Players',
              icon: Icons.person,
              imagePath: 'assets/images/players.jpg',
              route: Routes.players,
            ),
            buildCard(
              context: context,
              title: 'Matches',
              icon: Icons.sports_soccer,
              imagePath: 'assets/images/matches.jpg',
              route: Routes.matches,
            ),
            buildCard(
              context: context,
              title: 'Account',
              icon: Icons.settings,
              imagePath: 'assets/images/account.jpg',
              route: Routes.account_settings,
            ),
          ],
        ),
      ),
    );
  }
}
