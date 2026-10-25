import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True)  # Valve Hero ID (1 = Anti-Mage, 14 = Pudge, etc.)
    name = Column(String(64), nullable=False, unique=True)  # e.g. "npc_dota_hero_antimage"
    localized_name = Column(String(64), nullable=False)  # "Anti-Mage"
    localized_name_ru = Column(String(64), nullable=False)  # "Антимаг"
    primary_attr = Column(String(16), nullable=False)  # "agi", "str", "int", "all"
    attack_type = Column(String(16), nullable=False)  # "Melee", "Ranged"
    roles = Column(String(256), default="")  # e.g. "Carry,Escape,Nuker"
    icon_url = Column(String(256), nullable=False)  # Steam CDN URL
    aliases = Column(String(512), default="")  # Comma-separated CIS slang & nicknames

    # Relationships
    role_stats = relationship("RoleStat", back_populates="hero", cascade="all, delete-orphan")
    matchups = relationship("Matchup", foreign_keys="Matchup.hero_id", back_populates="hero", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "localized_name": self.localized_name,
            "localized_name_ru": self.localized_name_ru,
            "primary_attr": self.primary_attr,
            "attack_type": self.attack_type,
            "roles": [r.strip() for r in self.roles.split(",") if r.strip()],
            "icon_url": self.icon_url,
            "aliases": [a.strip() for a in self.aliases.split(",") if a.strip()],
        }


class RoleStat(Base):
    """Stores meta stats per role (Position 1-5) from Dota 2 Pro Tracker (D2PT)"""
    __tablename__ = "role_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id", ondelete="CASCADE"), nullable=False)
    role = Column(Integer, nullable=False)  # 1: Safe, 2: Mid, 3: Off, 4: Soft, 5: Hard
    matches = Column(Integer, default=0)
    winrate = Column(Float, default=50.0)  # Percentage (e.g. 53.4)
    pickrate = Column(Float, default=0.0)  # Percentage of matches
    tier = Column(String(8), default="B")  # "S", "A", "B", "C", "D"
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    hero = relationship("Hero", back_populates="role_stats")

    __table_args__ = (
        UniqueConstraint("hero_id", "role", name="uix_hero_role"),
        Index("idx_role_stats_role_wr", "role", "winrate"),
    )

    def to_dict(self):
        return {
            "hero_id": self.hero_id,
            "role": self.role,
            "matches": self.matches,
            "winrate": round(self.winrate, 2),
            "pickrate": round(self.pickrate, 2),
            "tier": self.tier,
        }


class Matchup(Base):
    """
    Stores pairwise hero counter advantage and synergy.
    hero_id vs_hero_id:
      - advantage: > 0 means hero_id is favored against vs_hero_id (counter advantage)
                   < 0 means hero_id is countered by vs_hero_id
      - winrate: hero_id's winrate when playing against vs_hero_id
      - synergy: bonus winrate when hero_id and vs_hero_id are on the same team
    """
    __tablename__ = "matchups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id", ondelete="CASCADE"), nullable=False)
    vs_hero_id = Column(Integer, ForeignKey("heroes.id", ondelete="CASCADE"), nullable=False)
    advantage = Column(Float, default=0.0)  # Percentage advantage
    winrate = Column(Float, default=50.0)   # Direct vs winrate
    games_played = Column(Integer, default=50) # Sample size for Bayesian smoothing
    synergy = Column(Float, default=0.0)    # Synergy % when on same team
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    hero = relationship("Hero", foreign_keys=[hero_id], back_populates="matchups")

    __table_args__ = (
        UniqueConstraint("hero_id", "vs_hero_id", name="uix_hero_vs_hero"),
        Index("idx_matchup_hero_vs", "hero_id", "vs_hero_id"),
    )

    def to_dict(self):
        return {
            "hero_id": self.hero_id,
            "vs_hero_id": self.vs_hero_id,
            "advantage": round(self.advantage, 2),
            "winrate": round(self.winrate, 2),
            "games_played": self.games_played,
            "synergy": round(self.synergy, 2),
        }
