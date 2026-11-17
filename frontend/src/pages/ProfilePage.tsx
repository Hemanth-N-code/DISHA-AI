// frontend/src/pages/ProfilePage.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  User, GraduationCap, Sparkles, Check, Save, Sliders,
  BookOpen, Star, Plus, Trash2, ArrowRight, ShieldCheck, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { StudentProfile, SkillItem } from '../types';

export const ProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);

  // Form states
  const [stream, setStream] = useState<string>('Science (PCM)');
  const [marks, setMarks] = useState<number>(85);
  const [programming, setProgramming] = useState<'none' | 'low' | 'moderate' | 'high'>('low');
  const [math, setMath] = useState<'low' | 'moderate' | 'high'>('moderate');
  const [creativity, setCreativity] = useState<'low' | 'moderate' | 'high'>('high');
  const [people, setPeople] = useState<'low' | 'balanced' | 'high'>('balanced');

  const [interests, setInterests] = useState<string[]>([]);
  const [newInterest, setNewInterest] = useState<string>('');

  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [newSkillName, setNewSkillName] = useState<string>('');
  const [newSkillLevel, setNewSkillLevel] = useState<number>(3);

  const [goals, setGoals] = useState<string[]>([]);
  const [constraints, setConstraints] = useState<string[]>([]);

  useEffect(() => {
    setLoading(true);
    api.profile.get()
      .then((data) => {
        setProfile(data);
        setStream(data.stream || 'Science (PCM)');
        setMarks(data.marks_percentage || 85);
        setProgramming(data.programming_preference || 'low');
        setMath(data.mathematics_preference || 'moderate');
        setCreativity(data.creativity_level || 'high');
        setPeople(data.people_interaction_preference || 'balanced');
        setInterests(data.interests || []);
        setSkills(data.skills || []);
        setGoals(data.goals || []);
        setConstraints(data.constraints || []);
      })
      .catch((err) => {
        console.warn('Profile not found, defaulting:', err);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSaveSuccess(false);

    try {
      const payload = {
        education_level: '12th_standard',
        stream,
        marks_percentage: marks,
        programming_preference: programming,
        mathematics_preference: math,
        creativity_level: creativity,
        people_interaction_preference: people,
        interests,
        skills,
        goals,
        constraints,
      };

      const updated = await api.profile.createOrUpdate(payload);
      setProfile(updated);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to save profile:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleAddInterest = () => {
    if (newInterest.trim() && !interests.includes(newInterest.trim())) {
      setInterests([...interests, newInterest.trim()]);
      setNewInterest('');
    }
  };

  const handleRemoveInterest = (item: string) => {
    setInterests(interests.filter((i) => i !== item));
  };

  const handleAddSkill = () => {
    if (newSkillName.trim() && !skills.some((s) => s.skill.toLowerCase() === newSkillName.trim().toLowerCase())) {
      setSkills([...skills, { skill: newSkillName.trim(), level: newSkillLevel }]);
      setNewSkillName('');
      setNewSkillLevel(3);
    }
  };

  const handleRemoveSkill = (skillName: string) => {
    setSkills(skills.filter((s) => s.skill !== skillName));
  };

  const handleUpdateSkillLevel = (skillName: string, level: number) => {
    setSkills(skills.map((s) => (s.skill === skillName ? { ...s, level } : s)));
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200 uppercase tracking-wider">
                  Deterministic Calibration Profile
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 font-medium border border-emerald-200 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" /> 5-Pillar Compatibility Anchor
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <User className="w-7 h-7 text-brand-600" />
                Student Decision Profile
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-2xl">
                Tune your academic background, current skill proficiencies, and personal preferences. Changes here recalibrate compatibility across the entire 118-career universe.
              </p>
            </div>

            <Link
              to="/discover"
              className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2.5 px-4 rounded-xl text-sm transition-colors shadow-sm self-start md:self-auto"
            >
              Explore Matches <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* AI Archetype & Strengths Card */}
        {profile && profile.profile_summary && (
          <div className="bg-gradient-to-r from-brand-900 via-indigo-950 to-slate-900 rounded-2xl p-6 text-white shadow-lg space-y-3">
            <div className="flex items-center gap-2 text-brand-300 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-amber-300" /> Synthesized Profile Archetype
            </div>
            <p className="text-sm sm:text-base text-brand-100 leading-relaxed font-medium">
              "{profile.profile_summary}"
            </p>
            {profile.academic_strengths && (
              <div className="flex flex-wrap gap-2 pt-1">
                {profile.academic_strengths.map((str, i) => (
                  <span
                    key={i}
                    className="text-xs bg-white/10 text-white border border-white/15 px-3 py-1 rounded-lg font-medium"
                  >
                    ✓ {str}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Profile Edit Form */}
        <form onSubmit={handleSaveProfile} className="space-y-8">
          {/* Section 1: Academic Background */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <GraduationCap className="w-5 h-5 text-brand-600" />
              1. Academic Foundation
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                  Stream / Educational Track
                </label>
                <select
                  value={stream}
                  onChange={(e) => setStream(e.target.value)}
                  className="w-full text-sm bg-slate-50 border border-slate-300 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
                >
                  <option value="Science (PCM)">Science (PCM - Physics, Chemistry, Math)</option>
                  <option value="Science (PCB)">Science (PCB - Physics, Chemistry, Biology)</option>
                  <option value="Science (PCMB)">Science (PCMB - Combined)</option>
                  <option value="Commerce">Commerce (Accounts, Business Studies, Economics)</option>
                  <option value="Arts / Humanities">Arts / Humanities (History, Political Science, Psychology)</option>
                  <option value="Vocational / Polytechnic">Vocational / Polytechnic Diploma</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                  12th / PUC Marks Percentage: {marks}%
                </label>
                <input
                  type="range"
                  min={50}
                  max={100}
                  value={marks}
                  onChange={(e) => setMarks(Number(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600 mt-3"
                />
                <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                  <span>50%</span>
                  <span>75%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Preferences & Cognitive Sliders */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Sliders className="w-5 h-5 text-brand-600" />
              2. Core Orientations & Preferences
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Programming */}
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-2">
                  <span>Programming Comfort</span>
                  <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                    {programming}
                  </span>
                </div>
                <div className="grid grid-cols-4 gap-1 bg-slate-100 p-1 rounded-xl">
                  {(['none', 'low', 'moderate', 'high'] as const).map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setProgramming(opt)}
                      className={`text-xs py-2 font-medium rounded-lg capitalize transition-all ${
                        programming === opt
                          ? 'bg-white text-brand-700 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              {/* Mathematics */}
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-2">
                  <span>Mathematics Comfort</span>
                  <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                    {math}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                  {(['low', 'moderate', 'high'] as const).map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setMath(opt)}
                      className={`text-xs py-2 font-medium rounded-lg capitalize transition-all ${
                        math === opt
                          ? 'bg-white text-brand-700 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              {/* Creativity */}
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-2">
                  <span>Creativity & Design Focus</span>
                  <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                    {creativity}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                  {(['low', 'moderate', 'high'] as const).map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setCreativity(opt)}
                      className={`text-xs py-2 font-medium rounded-lg capitalize transition-all ${
                        creativity === opt
                          ? 'bg-white text-brand-700 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              {/* People Interaction */}
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-2">
                  <span>People & Team Interaction</span>
                  <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                    {people}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                  {(['low', 'balanced', 'high'] as const).map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setPeople(opt)}
                      className={`text-xs py-2 font-medium rounded-lg capitalize transition-all ${
                        people === opt
                          ? 'bg-white text-brand-700 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Skills with 1-5 Ratings */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <Star className="w-5 h-5 text-brand-600" />
                  3. Current Skill Proficiencies (1 to 5)
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  1 = Novice, 3 = Competent, 5 = Master / Expert
                </p>
              </div>
            </div>

            {/* Existing Skills List */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {skills.map((s) => (
                <div
                  key={s.skill}
                  className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between"
                >
                  <div>
                    <span className="text-sm font-bold text-slate-800">{s.skill}</span>
                    <div className="flex items-center gap-1 mt-1">
                      {[1, 2, 3, 4, 5].map((lvl) => (
                        <button
                          key={lvl}
                          type="button"
                          onClick={() => handleUpdateSkillLevel(s.skill, lvl)}
                          className={`w-6 h-6 rounded-md text-xs font-bold transition-all ${
                            lvl <= s.level
                              ? 'bg-brand-600 text-white'
                              : 'bg-slate-200 text-slate-600 hover:bg-slate-300'
                          }`}
                        >
                          {lvl}
                        </button>
                      ))}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(s.skill)}
                    className="text-slate-400 hover:text-rose-600 p-1"
                    title="Remove skill"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>

            {/* Add Skill Row */}
            <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
              <input
                type="text"
                placeholder="Add skill (e.g. Python, Figma, Analytical Reasoning)..."
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                className="flex-1 text-xs px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500">Level:</span>
                <select
                  value={newSkillLevel}
                  onChange={(e) => setNewSkillLevel(Number(e.target.value))}
                  className="text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-800"
                >
                  <option value={1}>1 - Beginner</option>
                  <option value={2}>2 - Elementary</option>
                  <option value={3}>3 - Intermediate</option>
                  <option value={4}>4 - Advanced</option>
                  <option value={5}>5 - Expert</option>
                </select>
                <button
                  type="button"
                  onClick={handleAddSkill}
                  className="text-xs bg-slate-800 hover:bg-slate-900 text-white font-semibold px-4 py-2.5 rounded-xl transition-colors"
                >
                  Add Skill
                </button>
              </div>
            </div>
          </div>

          {/* Section 4: Interests */}
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-brand-600" />
              4. Extracurricular Interests & Curiosity Areas
            </h2>

            <div className="flex flex-wrap gap-2">
              {interests.map((interest) => (
                <span
                  key={interest}
                  className="inline-flex items-center gap-1.5 text-xs bg-brand-50 text-brand-700 border border-brand-200 px-3 py-1.5 rounded-xl font-medium"
                >
                  {interest}
                  <button
                    type="button"
                    onClick={() => handleRemoveInterest(interest)}
                    className="hover:text-brand-900 font-bold ml-1"
                  >
                    &times;
                  </button>
                </span>
              ))}
            </div>

            <div className="flex gap-2 max-w-md">
              <input
                type="text"
                placeholder="e.g. Space Exploration, Sketching, Robotics..."
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                className="flex-1 text-xs px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
              <button
                type="button"
                onClick={handleAddInterest}
                className="text-xs bg-slate-800 hover:bg-slate-900 text-white font-semibold px-4 py-2 rounded-xl"
              >
                Add
              </button>
            </div>
          </div>

          {/* Save Action Bar */}
          <div className="flex items-center justify-between pt-4">
            {saveSuccess ? (
              <p className="text-sm font-semibold text-emerald-600 flex items-center gap-1.5">
                <Check className="w-4 h-4" /> Profile updated successfully! Recalibrating career universe...
              </p>
            ) : (
              <p className="text-xs text-slate-500">
                All weights adhere to DISHA's 5-pillar compatibility architecture.
              </p>
            )}

            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-6 rounded-xl text-sm transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
            >
              {saving ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Updating...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save Calibration Profile
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
