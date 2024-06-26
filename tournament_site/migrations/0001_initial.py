# Generated by Django 5.0.6 on 2024-06-01 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alliance_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('time', models.TimeField(default='00:00:00')),
                ('side1RankingPoints', models.IntegerField(default=0)),
                ('side2RankingPoints', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_number', models.IntegerField(unique=True)),
                ('field_name', models.CharField(max_length=100)),
                ('side1', models.CharField(max_length=100)),
                ('side2', models.CharField(max_length=100)),
                ('matches', models.ManyToManyField(blank=True, to='tournament_site.matches')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, unique=True)),
                ('ranking_points', models.IntegerField(default=0)),
                ('matches_played', models.IntegerField(default=0)),
                ('alliance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament_site.team')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100)),
                ('number_of_teams', models.IntegerField(default=0)),
                ('teams', models.ManyToManyField(to='tournament_site.team')),
            ],
        ),
        migrations.CreateModel(
            name='PlayoffMatches',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('side1Team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='side1TeamPlayoff', to='tournament_site.team')),
                ('side2Team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='side2TeamPlayoff', to='tournament_site.team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='tournament_site.team')),
            ],
        ),
        migrations.AddField(
            model_name='matches',
            name='side1Team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side1Team1', to='tournament_site.team'),
        ),
        migrations.AddField(
            model_name='matches',
            name='side1Team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side1Team2', to='tournament_site.team'),
        ),
        migrations.AddField(
            model_name='matches',
            name='side2Team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side2Team1', to='tournament_site.team'),
        ),
        migrations.AddField(
            model_name='matches',
            name='side2Team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side2Team2', to='tournament_site.team'),
        ),
        migrations.CreateModel(
            name='Bracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Finals', models.ManyToManyField(blank=True, related_name='Finals', to='tournament_site.playoffmatches')),
                ('Quarterfinals', models.ManyToManyField(blank=True, related_name='Quarterfinals', to='tournament_site.playoffmatches')),
                ('Semifinals', models.ManyToManyField(blank=True, related_name='Semifinals', to='tournament_site.playoffmatches')),
                ('Winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Winner', to='tournament_site.team')),
            ],
        ),
    ]
