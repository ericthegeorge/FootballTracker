import 'package:flutter/material.dart';
import 'package:frontend/routes.dart';

class MainSelectionScreen extends StatelessWidget {
  void navigateToScreen(BuildContext context, String screen) {
    switch (screen) {
      case 'league':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => LeagueScreen()),
        );
        break;
      case 'team':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => TeamScreen()),
        );
        break;
      case 'player':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => PlayerScreen()),
        );
        break;
      case 'matches':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => MatchesScreen()),
        );
        break;
      case 'account_settings':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => AccountSettingsScreen()),
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

// Dummy screens for each option
class LeagueScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('League Screen')),
      body: Center(child: Text('This is the League screen')),
    );
  }
}

class TeamScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Team Screen')),
      body: Center(child: Text('This is the Team screen')),
    );
  }
}

class PlayerScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Player Screen')),
      body: Center(child: Text('This is the Player screen')),
    );
  }
}

class MatchesScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Matches Screen')),
      body: Center(child: Text('This is the Matches screen')),
    );
  }
}

class AccountSettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Account Settings Screen')),
      body: Center(child: Text('This is the Account Settings screen')),
    );
  }
}
